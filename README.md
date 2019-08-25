# Scraper for www.createdebate.com

## Functionality
This scraper and the utility scripts here can be used to scrape debates and user information from CreateDebate.

## Usage
	get_all_debate_motion.py - We scrape the list of OPEN DEBATES from the ALL TOPICS Tab at the Website.
				   Assigns a uuid to each debate and stores in a dictionary 'dict_motion2uuid' 
				   and text file 'data_Motion2uuid.txt'.

	get_all_motions_topicwise - We scrape the list of OPEN DEBATES from the different topic tabs one by one.
				    Assign a uuid to those debate motions which were not present in 'dict_motion2uuid'
				    Then create text files for each topic to store the motions topic wise.
				    Also create dictionaries: 'dict_motion2topic' and 'dict_topic2motion'.

	get_all_responses - We then create the debate urls for each debate motion and fetch the response of that page
			    and store it in a serialized binary file in 'Debate_Responses'.

	parse_sidestances - We parse the response files to extract the L-R stances and store in 'dict_motion2sidestances'.

	parse_arguments - We parse the response files to extract the argument parameters and store in 'Debate_Arguments'.

	compose_user_data - We scan through all the files in 'Debate_Arguments' and compile all the arguments userwise.
			    Also assign a uuid to all the usernames and store in dictionary 'dict_user2uuid'
			    and text file 'data_User2uuid.txt'

	get_all_user_profile - We then create profile urls for each user name and fetch the response of that page and 
	                       store it in a serialized binary file in 'UserProfile_Responses'.

	parse_user_params - We parse the response files to extract information and details of the user and 
			    store in 'data_UserInformation.txt'.

## Formats

### Dictionaries
	motion2uuid  		=> {motion    : uuid 		}
	motion2topic 		=> {motion    : [topics]	}
	topic2motion 		=> {topic     : [motions]	}
	motion2sidesstances 	=> {motion    : [sideL, sideR]	}
	user2uuid    		=> {user_name : uuid 		}

### Text Files
	data_Motion2uuid.txt 	 => "\t".join(["motion"   , "uuid"])
	data_User2uuid.txt   	 => "\t".join(["user_name", "uuid"])
	data_UserInformation.txt => "\t".join(["UserName", "Name", "Gender", "Age", "MaritalStatus", "PoliticalParty",
					       "Country", "Religion", "Education", "Points", "Efficiency", "Arguments",
					       "Debates", "Joined"])

### Directories
	Topicwise_Motions     => ["Politics", "Entertainment", "World", "Religion", "Law", "Science", "Technology", 
				  "Sports", "Comedy", "Business", "Travel", "Shopping", "Health", "NSFW"] 
				  and "None" for motions without any assigned topic.	 				  
	within each file      => "\t".join(["motion", "uuid"])

	Debate_Respones       => ["DebateUUID" for UUID in motion2uuid.values()] binary files.

	Debate_Arguments      => ["DebateUUID.txt" for UUID in motion2uuid.values()] text files.
	within each file      => "\t".join(["DebateMotion", "ArgumentSide", "UserName", "Time", "ArgumentStance", 
					    "Votes", "Post"])

	User_Arguments        => ["UserUUID.txt" for UUID in user2uuid.values()] text files
	within each file      => "\t".join(["UserName", "DebateMotion", "ArgumentSide", "ArgumentStance", "Votes",
					    "Time", "Post"])

	UserProfile_Responses => ["UserUUID" for UUID in user2uuid.values()] binary files



