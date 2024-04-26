<script>
import axios from 'axios'
export default {
    name: "Menu",
    props: { user: Number },
    data() {
        return {
            games: [],
            count: 0
        }
    },
    mounted() {
        this.init()
    },
    methods: {

        async init() {
            const api = axios.create({
                baseURL: 'http://127.0.0.1:5000',
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                timeout: 10000
            })
            const response = await api.get('/getGames')
            this.games = response.data.result
            this.count = this.games.length

        },
        search() {
            for (var i = 0; i < this.count; i++) {
                if (this.games[i].title.toLowerCase().includes(document.getElementById("search").value.toLowerCase())) {
                    document.getElementById('element' + (i + 1)).style.display = "block"
                }
                else {
                    document.getElementById('element' + (i + 1)).style.display = "none"
                }
            }
        },
        async selectGame(i) {
            console.log(this.games[i - 1]._id)
            this.$emit("selectedGame", this.games[i - 1]._id)
            const api = axios.create({
                baseURL: 'http://127.0.0.1:5000',
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                timeout: 10000
            });

            const response = await api.get('/getGameState/' + this.game);
            this.$emit("changeState", response.data.result)
        },
        SignIn() {
            this.$emit("changeState", 0)
        }

    }
}
</script>

<template>
    <v-toolbar style="position: absolute; top:0%; left: 0%; height: 7% ;">
        <v-btn @click="search()">
            <v-icon>mdi-magnify</v-icon>
        </v-btn>
        <v-text-field single-line hide-details id="search" @input="search()"></v-text-field>

        <button class="btn" type="button" @click="SignIn()">Log Out</button>
    </v-toolbar>

    <v-container style=" position: absolute; left:5%;right: 5%; background-color: aliceblue; top:8%;">
        <v-row>
            <v-col v-for="i in count" :key="i" cols="3" :id="'element' + i">
                <v-card class="mx-auto" max-width="400" height="400" @click="selectGame(i)">

                    <v-img :src="'http://127.0.0.1:5000/getImageById/' + games[i - 1].image" height="200px" cover></v-img>
                    <v-card-title>{{ games[i - 1].title }}</v-card-title>
                    <v-card-text>{{ games[i - 1].description }}</v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped>
.btn {
    background-color: rgba(11, 78, 29, 0.525);
    color: aliceblue;
    width: 10%;
    border: none;
    cursor: pointer;
    padding: 14px 20px;
    margin: 10px;
}

.btn:hover {
    opacity: 0.8;
}
</style>