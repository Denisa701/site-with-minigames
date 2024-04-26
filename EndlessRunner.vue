<script>
import axios from 'axios'
import * as THREE from 'three'
import {CSS2DRenderer, CSS2DObject} from "three/examples/jsm/renderers/CSS2DRenderer.js"


export default {
    name: "Highscores",
    props: { game: String },
    data() {
        return {
            title: '',
            playerSpeed: 0.1,
            spawnPoint: new THREE.Vector3(5, -1.25, 1),
            keyboard: {},
            time: 0,
            sprites: [],
            playerState: 0,
            playerCount: 0
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            // GET TITLE 
            // const api = axios.create({
            //     baseURL: 'http://127.0.0.1:5000',
            //     headers: {
            //         'Content-Type': 'multipart/form-data'
            //     },
            //     timeout: 10000
            // })
            // const response = await api.get('/getGameTitle/' + this.game)
            // this.title = response.data.result
            // console.log(this.tittle)

            // Endless runner

            window.addEventListener('keydown', this.keyDown)
            window.addEventListener('keydown', this.keyDown)
            // Create scene

            this.scene = new THREE.Scene()

            // Get Clock
            this.clock = new THREE.Clock()

            // Create camera

            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
            this.camera.position.y = 1.5
            this.camera.position.z = 5
            this.camera.position.x = 0
            this.camera.lookAt(new THREE.Vector3(0,1.5,0))

            // Background
            var textureLoader = new THREE.TextureLoader()
            var background = textureLoader.load('/background2d.jpg')
            textureLoader.wrapS = THREE.RepeatWrapping

            this.bkgmesh = new THREE.Mesh( 
                new THREE.PlaneGeometry(20,10, 100, 100),
                new THREE.MeshBasicMaterial({
                        map: background
                    })
            )

            this.bkgmesh.position.y = 1
    
            this.scene.add(this.bkgmesh)  

            // Player
        
            this.sprites.push(textureLoader.load('/1.png'))
            this.sprites.push(textureLoader.load('/2.png'))
            this.sprites.push(textureLoader.load('/3.png'))
            this.sprites.push(textureLoader.load('/4.png'))

            this.playerMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(1,1,50,50),
                new THREE.MeshBasicMaterial({
                    map: this.sprites[this.playerState],
                    transparent:true 
                })
            )

            this.playerMesh.position.z = 1
            this.playerMesh.position.x = -3.5
            this.playerMesh.position.y = -1
            this.scene.add(this.playerMesh)

            // obstacle
            this.rock = new THREE.Mesh(
                new THREE.PlaneGeometry(1,1,50,50),
                new THREE.MeshBasicMaterial({
                    map:  textureLoader.load('/rock.png'),
                    transparent: true
                })
            )

            this.rock.position.x = this.spawnPoint.x
            this.rock.position.y = this.spawnPoint.y
            this.rock.position.z = this.spawnPoint.z
            this.scene.add(this.rock)

                // text- time renderer
            this.timerDiv = document.createElement('div')
            this.timerDiv.id = 'timerDiv'
            this.timerDiv.textContent = 'time: 0'
            this.timerDiv.style.backgroundColor = ' transparent'
            this.timerDiv.style.fontSize = '30px'
            
            const timerLabel = new CSS2DObject(this.timerDiv)
            timerLabel.position.set(0,0,0)
            this.scene.add(timerLabel)
            timerLabel.layers.set(0)
            
            this.labelrenderer = new CSS2DRenderer()
            
            this.labelrenderer.setSize(window.innerWidth * 15/100, window.innerHeight * 5/100)
            
            this.labelrenderer.domElement.id = "labelrenderer"
            this.labelrenderer.domElement.style.position = "absolute"
            this.labelrenderer.domElement.style.left ="5%"
            this.labelrenderer.domElement.style.top = "10%"
            document.body.appendChild(this.labelrenderer.domElement)   

            // renderer setup
            this.renderer = new THREE.WebGLRenderer()
            this.renderer.setSize(window.innerWidth * 90/100, window.innerHeight *90/100)
            
            this.renderer.domElement.id = "canvas"
            this.renderer.domElement.style.position = "absolute"
            this.renderer.domElement.style.left ="5%"
            this.renderer.domElement.style.right = "5%"
            this.renderer.domElement.style.top = "10%"
            document.body.appendChild(this.renderer.domElement)

            this.animate()
        },
        animate(){
            requestAnimationFrame(this.animate)

            this.delta = this.clock.getDelta()
            this.bkgmesh.material.map.offset.x += 0.1 * this.delta
            this.time += this.delta
            this.timerDiv.textContent = "time" + this.time.toFixed(1).toString()

            this.playerCount += this.delta
            
            // obstacle movement
            this.rock.position.x -= this.playerSpeed * this.delta * 10
            
            // player speedUP
            if(this.playerCount >= 1){
                this.playerCount = 0
                this.playerState +=1
                this.playerState %=4
                this.playerMesh.material.map = this.sprites[this.playerState]
            }

            if(this.keyboard[39]){
                if(this.playerSpeed < 0.5){

                    this.playerSpeed += 2 * this.delta
                }
            }
            else{
                if(this.playerSpeed > 0.1){

                    this.playerSpeed -= 5* this.delta
                }
            }

            if(this.rock.position.x < -5){
                this.rock.material.dispose()
                this.rock.geometry.dispose()
                this.rock.removeFromParent()
            }

            // player colision
            var playerBoundingBox = new THREE.Box3().setFromObject(this.playerMesh)
            var rockBoundingBox = new THREE.Box3().setFromObject(this.rock)
            var collision = playerBoundingBox.intersectsBox(rockBoundingBox)

            if(collision ==true)
            {
                console.log("game over")
            }

            this.renderer.render(this.scene, this.camera)
            this.labelrenderer.render(this.scene, this.camera)
        },
        keyDown(event){
            this.keyboard[event.keyCode] = true;

        },
        keyUp(event){
            this.keyboard[event.keyCode] = false;
        },
        // return to main Menu
        mainMenu() {
            this.$emit("changeState", 2)
            document.getElementById('canvas').remove()
            document.getElementById('labelrenderer').remove()
            // document.getElementById('timerDiv').remove()
        },
        toScores() {
            this.$emit("changeState", 3)
            document.getElementById('canvas').remove()
            document.getElementById('timerLabel').remove()
            document.getElementById('timerDiv').remove()
        },
        SignIn() {
            this.$emit("changeState", 0)
            document.getElementById('canvas').remove()
            document.getElementById('timerLabel').remove()
            document.getElementById('timerDiv').remove()
        }
    }
}

</script>

<template>
    <v-toolbar style="position: absolute; top:0%; left: 0%; height: 7% ;">

        <v-app-bar-tittle>{{ this.title }}</v-app-bar-tittle>
        <button class="btn" type="button" @click="SignIn()">Log Out</button>
        <button class="btn" type="button" @click="mainMenu()">Back to Menu</button>
        <button class="btn" @click="toScores()">To the Highscores</button>
        
    </v-toolbar>
    <span v-text="this.title"></span>

    <v-container style=" position: absolute; left:5%;right: 5%; background-color: aliceblue; top:8%;">

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