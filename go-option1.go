package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/gmail/v1"
	"google.golang.org/api/option"
)

func main() {
	// Get sender email addresses from command-line arguments
	senders := os.Args[1:]
	if len(senders) == 0 {
		fmt.Println("No senders provided. Pass email addresses as arguments.")
		return
	}

	// Authenticate and create Gmail service
	srv, err := getGmailService()
	if err != nil {
		log.Fatalf("Unable to create Gmail client: %v\n", err)
	}

	// Process each sender concurrently
	var wg sync.WaitGroup
	for _, sender := range senders {
		wg.Add(1)
		go func(sender string) {
			defer wg.Done()
			processSender(context.Background(), srv, sender)
		}(sender)
	}

	wg.Wait()
	fmt.Println("All selected senders processed successfully.")
}

func getGmailService() (*gmail.Service, error) {
	// Read the credentials file
	b, err := os.ReadFile("credentials.json")
	if err != nil {
		return nil, fmt.Errorf("unable to read client secret file: %v", err)
	}

	// Parse the credentials file
	config, err := google.ConfigFromJSON(b, gmail.GmailModifyScope, gmail.GmailSettingsBasicScope)
	if err != nil {
		return nil, fmt.Errorf("unable to parse client secret file to config: %v", err)
	}

	// Get an authenticated client
	client := getClient(config)

	// Create a Gmail service
	return gmail.NewService(context.Background(), option.WithHTTPClient(client))
}

func getClient(config *oauth2.Config) *http.Client {
	// Token file to store the user's credentials
	const tokenFile = "token.json"

	// Try to load the token from file
	tok, err := tokenFromFile(tokenFile)
	if err != nil {
		// Authenticate user if token is not available
		tok = getTokenFromWeb(config)
		saveToken(tokenFile, tok)
	}

	return config.Client(context.Background(), tok)
}

func tokenFromFile(file string) (*oauth2.Token, error) {
	f, err := os.Open(file)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	tok := &oauth2.Token{}
	err = json.NewDecoder(f).Decode(tok)
	return tok, err
}

func getTokenFromWeb(config *oauth2.Config) *oauth2.Token {
	authURL := config.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
	fmt.Printf("Go to the following link in your browser then type the authorization code:\n%v\n", authURL)

	var authCode string
	fmt.Print("Enter the authorization code: ")
	if _, err := fmt.Scan(&authCode); err != nil {
		log.Fatalf("Unable to read authorization code: %v", err)
	}

	tok, err := config.Exchange(context.TODO(), authCode)
	if err != nil {
		log.Fatalf("Unable to retrieve token from web: %v", err)
	}
	return tok
}

func saveToken(path string, token *oauth2.Token) {
	fmt.Printf("Saving credential file to: %s\n", path)
	f, err := os.Create(path)
	if err != nil {
		log.Fatalf("Unable to save oauth token: %v", err)
	}
	defer f.Close()
	json.NewEncoder(f).Encode(token)
}

func fetchEmails(ctx context.Context, srv *gmail.Service, sender string) ([]string, error) {
	query := fmt.Sprintf("from:%s", sender)
	res, err := srv.Users.Messages.List("me").Q(query).Do()
	if err != nil {
		return nil, err
	}

	var messageIDs []string
	for _, msg := range res.Messages {
		messageIDs = append(messageIDs, msg.Id)
	}
	return messageIDs, nil
}

func createLabel(ctx context.Context, srv *gmail.Service, labelName string) (string, error) {
	labels, err := srv.Users.Labels.List("me").Do()
	if err != nil {
		return "", err
	}

	// Check if the label already exists
	for _, label := range labels.Labels {
		if label.Name == labelName {
			return label.Id, nil
		}
	}

	// Create the label if it doesn't exist
	label := &gmail.Label{
		Name:                 labelName,
		LabelListVisibility:  "labelShow",
		MessageListVisibility: "show",
	}

	res, err := srv.Users.Labels.Create("me", label).Do()
	if err != nil {
		return "", err
	}
	return res.Id, nil
}

func moveEmails(ctx context.Context, srv *gmail.Service, messageIDs []string, labelID string) error {
	for _, msgID := range messageIDs {
		_, err := srv.Users.Messages.Modify("me", msgID, &gmail.ModifyMessageRequest{
			AddLabelIds:    []string{labelID},
			RemoveLabelIds: []string{"INBOX"},
		}).Do()
		if err != nil {
			return err
		}
	}
	return nil
}

func createFilter(ctx context.Context, srv *gmail.Service, sender string, labelID string) error {
	filter := &gmail.Filter{
		Criteria: &gmail.FilterCriteria{
			From: sender,
		},
		Action: &gmail.FilterAction{
			AddLabelIds:    []string{labelID},
			RemoveLabelIds: []string{"INBOX"},
		},
	}

	_, err := srv.Users.Settings.Filters.Create("me", filter).Do()
	return err
}


func processSender(ctx context.Context, srv *gmail.Service, sender string) {
	fmt.Printf("Processing emails for sender: %s\n", sender)

	// Fetch emails for the sender
	messageIDs, err := fetchEmails(ctx, srv, sender)
	if err != nil {
		fmt.Printf("Error fetching emails for %s: %v\n", sender, err)
		return
	}

	// Create or get the label
	labelID, err := createLabel(ctx, srv, "EmailTracker/Unsubscribe")
	if err != nil {
		fmt.Printf("Error creating label for %s: %v\n", sender, err)
		return
	}

	// Move emails to the label
	err = moveEmails(ctx, srv, messageIDs, labelID)
	if err != nil {
		fmt.Printf("Error moving emails for %s: %v\n", sender, err)
		return
	}

	// Create a Gmail filter for future emails
	err = createFilter(ctx, srv, sender, labelID)
	if err != nil {
		fmt.Printf("Error creating filter for %s: %v\n", sender, err)
		return
	}

	fmt.Printf("Finished processing sender: %s\n", sender)
}

// Fetch emails, createLabel, moveEmails, and createFilter functions remain unchanged.
