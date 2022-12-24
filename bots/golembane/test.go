func updateExistingCommand(w http.ResponseWriter, r *http.Request) {
	fmt.Println("Endpoint Hit: updateExistingCommand")
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

	/* Get Document by Filter */
	// collection := client.Database("feh").Collection("robin")
	// filter := bson.D{{"name", "calendar"}}
	// var result Command
	// err = collection.FindOne(context.TODO(), filter).Decode(&result)
	// fmt.Println(result)
	// fmt.Println(result.name)
	// fmt.Println(result.value)

	// robinResult, err := robinCollection.InsertOne(ctx, command)
	// if err != nil {
	// 	log.Fatal(err)
	// }

	// Print Return Statement
	// son.NewEncoder(w).Encode(command)
	fmt.Println("Endpoint Hit: updateExistingCommand")
}
