package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"github.com/gorilla/mux"
)

type Article struct {
	Id      string `json:"Id"`
	Title   string `json:"Title"`
	Desc    string `json:"desc"`
	Content string `json:"content"`
}

type Command struct {
	Name 	string
	Value string
}

type CommandDB struct {
	ID		primitive.ObjectID `bson:"_id"`
	Name 	string
	Value string
}

// let's declare a global Articles array
// that we can then populate in our main function
// to simulate a database
var Articles []Article

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the HomePage!")
	fmt.Println("Endpoint Hit: homePage")
}

func returnAllArticles(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: returnAllArticles")
	json.NewEncoder(w).Encode(Articles)
}

func createNewArticle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: createNewArticle")
	// get the body of our POST request
	// unmarshal this into a new Article struct
	// append this to our Articles array.    
	reqBody, _ := ioutil.ReadAll(r.Body)
	var article Article 
	json.Unmarshal(reqBody, &article)
	// update our global Articles array to include
	// our new Article
	Articles = append(Articles, article)
	json.NewEncoder(w).Encode(article)
}

func createNewCommand(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: createNewCommand")
	// get the body of our POST request
	// unmarshal this into a new Article struct
	// append this to our Articles array.    
	reqBody, _ := ioutil.ReadAll(r.Body)
	var command Command 
	json.Unmarshal(reqBody, &command)

	// Add command to our database
	// mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://root:pass12345@localhost"))
	if err != nil {
			log.Fatal(err)
	}
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
			log.Fatal(err)
	}
	defer client.Disconnect(ctx)

	/* List Get Robin Bot Collection */
	fehDatabase := client.Database("feh")
	robinCollection := fehDatabase.Collection("robin")
	robinResult, err := robinCollection.InsertOne(ctx, command)
	if err != nil {
		log.Fatal(err)
	}

	// Print Return Statement
	fmt.Println(command)
	fmt.Println(robinResult)
	json.NewEncoder(w).Encode(command)
}

func deleteArticle(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: deleteArticle")
	// once again, we will need to parse the path parameters
	vars := mux.Vars(r)
	// we will need to extract the `id` of the article we
	// wish to delete
	id := vars["id"]

	// we then need to loop through all our articles
	for index, article := range Articles {
			// if our id path parameter matches one of our
			// articles
			if article.Id == id {
					// updates our Articles array to remove the 
					// article
					Articles = append(Articles[:index], Articles[index+1:]...)
			}
	}
	fmt.Fprintf(w, "Successfully delete Article Id: " + id)
}

func returnSingleArticle(w http.ResponseWriter, r *http.Request){
	fmt.Println("Endpoint Hit: returnSingleArticle")
	vars := mux.Vars(r)
	key := vars["id"]
	// Loop over all of our Articles
	// if the article.Id equals the key we pass in
	// return the article encoded as JSON
	for _, article := range Articles {
		if article.Id == key {
				json.NewEncoder(w).Encode(article)
		}
	}
}

func updateExistingCommand(w http.ResponseWriter, r *http.Request){
	fmt.Println("Endpoint Hit: updateExistingCommand")
	// get the body of our POST request
	// unmarshal this into a new Article struct
	// append this to our Articles array.    
	reqBody, _ := ioutil.ReadAll(r.Body)
	var command Command 
	json.Unmarshal(reqBody, &command)
	cName 	:= command.Name
	cValue 	:= command.Value 

	// Add command to our database
	// mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://root:pass12345@localhost"))
	if err != nil {
			log.Fatal(err)
	}
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
			log.Fatal(err)
	}
	defer client.Disconnect(ctx)

	/* Get Document by Filter */
	collection := client.Database("feh").Collection("robin")
	filterFind := bson.D{{"name", cName}}
	var result CommandDB
	err = collection.FindOne(context.TODO(), filterFind).Decode(&result)
	if err != nil {
		panic(err)
	}
	fmt.Println(result.ID.Hex())
	fmt.Println(result.Name)
	fmt.Println(result.Value)

	/* Update Document by Id */
	id, _ := primitive.ObjectIDFromHex(result.ID.Hex())
	filterUpdate := bson.D{{"_id", id}}
	valueUpdate := bson.D{{"$set", bson.D{{"value", cValue}}}}
	resultUpdate, err := collection.UpdateOne(context.TODO(), filterUpdate, valueUpdate)
	if err != nil {
		panic(err)
	}
	fmt.Println(resultUpdate)

	// Return Statement
	returnStatement := "Successfully update command: ||" + cName + "|| with value: ||" + cValue + "||"
	fmt.Fprintf(w, returnStatement)
	fmt.Println(returnStatement)
}

// REST Endpoints
func handleRequests() {
	// Creates a new instance of a mux router
	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/", homePage)
	myRouter.HandleFunc("/all", returnAllArticles)
	myRouter.HandleFunc("/article", createNewArticle).Methods("POST")
	myRouter.HandleFunc("/article/{id}", deleteArticle).Methods("DELETE")
	myRouter.HandleFunc("/article/{id}", returnSingleArticle)
	myRouter.HandleFunc("/command", createNewCommand).Methods("POST")
	myRouter.HandleFunc("/command", updateExistingCommand).Methods("PATCH")
	log.Fatal(http.ListenAndServe(":4545", myRouter))
}

// Main Function
func main() {
	fmt.Println("Starting Server...")
	Articles = []Article{
		Article{Id: "1", Title: "Hello", Desc: "Article Description", Content: "Article Content"},
		Article{Id: "2", Title: "Hello 2", Desc: "Article Description", Content: "Article Content"},
	}
	handleRequests()
}
