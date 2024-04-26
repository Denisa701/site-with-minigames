<script>
import axios from 'axios'
export default {
    name: "Highscores",
    props: { game: String, user: Number },
    data() {
        return {
            highscoreCollection: [],
            scores: [],
            score: Math.floor(Math.random() * (100 - 50 + 1) + 50)
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        // return to main Menu
        mainMenu() {
            this.$emit("changeState", 2)
        },
        
        // when the page gets accesed it will display only the scores of the game selected
        async init() {
            try {
                const api = axios.create({
                    baseURL: 'http://127.0.0.1:5000',
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    timeout: 10000
                });

                const response = await api.get('/getScoreTable/' + this.game);
                
                this.scores = response.data.result


                this.highscoreCollection = (await api.get('/getScores/'+ this.game)).data.result;
               
            } catch (error) {
                console.error('An error occurred:', error);
            }
        },


        async updateScores() {
            this.score = Math.floor(Math.random() * (100 - 50 + 1) + 50)
            console.log("new score", this.score)
            const formData = new FormData()
            formData.append('gameID', this.game)
            formData.append('userID', this.user)
            formData.append('score', this.score)
            
            
            var position = -1 // user didn't play the game 
            
           
            //passes through every user in scores, if user exists and the score is higher, the position is saved
            for (var i = 0; i < this.highscoreCollection.length; i++) {
                
                if ((this.user == this.highscoreCollection[i].userID) && (this.game == this.highscoreCollection[i].gameID)) {
                    if (this.score > this.highscoreCollection[i].score) {
                        console.log(this.score,this.highscoreCollection[i].score)
                        position = i
                    } else {
                        position = -2 //the score is lower than the prevoius/the table doesn't change
                    }
                    break
                }
            }

            

            if (position == -1) {
                
                //the user has never played the game so its a new entry  
                //_______________________POST_______________________

                const response = await axios.post('http://127.0.0.1:5000/addScore/',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                
                this.scores.push({ 'gameID': this.game, 'score':this.score, 'userID': this.user })
                
            } else {
                
                if (position != -2) {
                    
                    //_______________________PUT_______________________
                   
                    const response = await axios.put('http://127.0.0.1:5000/addScore/',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });
                    

                    this.getScoreById(position)
                }
                else
                {
                    document.getElementById("search").textContent = "Nothing to be updated"; // Changed error message
                setTimeout(() => {
                    document.getElementById("search").textContent = "";
                }, 2000);
                }
            }
           
        },
        // a intermediar function used in updateScores
        // it gets the old score and changes it to the new score
        async getScoreById(index) {
            // this section connects to the RestAPI
           
            const api = axios.create({
                baseURL: 'http://127.0.0.1:5000',
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                timeout: 10000
            })
            
            // GET the score that the user got 
            const response = await api.get('/getScoresById/' + this.user)

           
            this.scores[index]['score'] = response.data.result
    
        }
    }

}
</script>

<template>
    <v-toolbar style="position: absolute; top:0%; left: 0%; height: 10% ;margin-bottom:20px;">
        <button type="button" @click="mainMenu()">Back to Menu</button>
        <button class="btn" @click="updateScores()">Add Score</button>
        <button class="btn" type="button" @click="Play()">Play</button>
        <button class="btn" type="button" @click="SignIn()">Log Out</button>
        <v-text-field id="search" ></v-text-field>
    </v-toolbar>

    <v-container style=" position: absolute; margin: 10px;
    height: 50%;
    width: 50%; left:5%;right: 5%; ; top:8%;">
        <table id="scores">
            <tr>
                <th>Username</th>
                <th>Score</th>
            </tr>
            <tr v-for="i in scores.length" :key="i">
                <td>{{ scores[i - 1].userID }}</td>
                <td>{{ scores[i - 1].score }}</td>
            </tr>
        </table>
    </v-container>
</template>

<style scoped>
button {
    background-color: rgba(11, 78, 29, 0.525);
    color: aliceblue;
    width: 100%;
    border: none;
    cursor: pointer;
    padding: 14px 20px;
    margin: 10px;
}

button:hover {
    opacity: 0.8;
}

.sth {

    margin: 10px;
    bottom: 0;
    right: 0%;
    height: 10%;
    width: 20%;
}



#scores {
    position: absolute;
    left: 0%;
    right: 0%;
    top: 10%;
    width: 50%;
    border-collapse: collapse;
}

#scores th,
#scores td {
    border: 1px solid green;
    padding: 8px;
    text-align: center;
}

;

#scores tr:nth-child(even) {
    background-color: aquamarine;
}

#scores tr:hover {
    background-color: darkmagenta;
}

#scores th {
    background-color: aqua;
    color: aliceblue;
}
</style>