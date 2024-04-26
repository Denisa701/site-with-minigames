<script setup>
import forgotPass from './components/forgotPassword.vue'
import Login from './components/Login.vue'
import Menu from './components/Menu.vue'
import Register from './components/Register.vue'
import Highscores from './components/highScores.vue'
import EndlRun from './components/EndlessRunner.vue'
import MadBallon from './components/BallonMadness.vue'
import RPS from './components/RPS.vue'
import XandO from '/components/XandO.vue'
</script>

<script>
export default {
  components: {
    Login,
    Menu,
    Register,
    Highscores, 
    RPS,
    XandO
  },
  data() {
    return {
      state: 0,
      game: '',
      user: 0
    }
  }
}
</script>


<template>
   <div v-if="state == -1">
    <forgotPass @changeState="state = $event" ></forgotPass>
  </div>
  <div v-if="state == 0">
    <Login @changeState="state = $event" @username="user = $event"></Login>
  </div>
  <div v-if="state == 1">
    <Register @changeState="state = $event" @username="user = $event"></Register>
  </div>
  <div v-if="state == 2">
    <Menu @changeState="state = $event" @selectedGame="game = $event"  ></Menu>
  </div>
  <div v-if="state == 3">
    <Highscores @changeState="state = $event" :game="game" :user="user"></Highscores>
  </div>
  <div v-if="state == 4">
    <MadBallon @changeState="state = $event" :game="game" :user="user"></MadBallon>
  </div>
  <div v-if="state == 5">
    <EndlRun @changeState="state = $event" :game="game" :user="user"></EndlRun>
  </div>
</template>


<style scoped>
html,
body {
  width: 100vw;
  margin: 0%;
}

#app {
  width: inherit;
}
</style>
