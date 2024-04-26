<script>
import axios from 'axios'
import * as THREE from 'three'
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer.js"
import { MTLLoader } from "three/examples/jsm/loaders/MTLLoader.js"
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader.js"

export default {
    name: "Highscores",
    props: { game: String },
    data() {
        return {
            title: '',
            gameFrozen: false,
            areBalloonsMoving: true,
            gun: [],
            mouseX: -1,
            mouseY: -1,
            bullets: [],
            ballons: [],
            bulletsBoundingBox: [],
            ballonsBoundingBox: [],
            balloonResources: [],
            loadedMaterials: [],
            loadedMesh: [],
            score: 0
        }
    },
    mounted() {
        this.init()
    },
    methods: {
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
        async init() {

            // Ballon Madness
            window.addEventListener('resize', this.resize)

            // Create scene
            this.scene = new THREE.Scene()

            // Get Clock
            this.clock = new THREE.Clock()

            // Create camera
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
            this.camera.position.y = 1.5
            this.camera.position.z = 5
            this.camera.position.x = 0
            this.camera.lookAt(new THREE.Vector3(0, 1, 0))

            // Lighting
            this.ambientLight = new THREE.AmbientLight(0xffffff, 0.2)
            this.scene.add(this.ambientLight)
            this.light = new THREE.PointLight(0xffffff, 0.8, 20)
            this.light.position.set(-3, 6, -3)
            this.light.castShadow = true
            this.light.shadow.camera.near = 0.1
            this.light.shadow.camera.far = 25
            this.scene.add(this.light)

            // Ground
            // var textureLoader = new THREE.TextureLoader()
            // var groundTexture = textureLoader.load('/grass.jpg', function (texture) {
            //     texture.wrapS = texture.wrapT = THREE.RepeatWrapping
            //     texture.offset.set(0, 0)
            //     texture.repeat.set(50, 50)
            // })
            // this.groundMesh = new THREE.Mesh(
            //     new THREE.PlaneGeometry(100, 50, 1000, 1000),
            //     new THREE.MeshBasicMaterial({
            //         map: groundTexture
            //     })
            // )


            // this.groundMesh.position.y = -0.5
            // this.groundMesh.receiveShadow = false
            // this.scene.add(this.groundMesh)
            // rotirea groundului sa fie la sol

            // Sky 
            var textureLoader = new THREE.TextureLoader()
            var skyTexture = textureLoader.load('/cumulus-cloud.jpg')
            this.skyMesh = new THREE.Mesh(
                new THREE.PlaneGeometry(100, 50, 1000, 1000),
                new THREE.MeshBasicMaterial({
                    map: skyTexture
                })
            )
            this.skyMesh.position.y = -0.5
            this.skyMesh.receiveShadow = false
            this.scene.add(this.skyMesh)

            // Walls
            var wallTexture = textureLoader.load('/crate0_diffuse.png')
            this.placeWall(wallTexture, 5, 8, 1, 0, 0, 1)
            this.placeWall(wallTexture, 5, 1, 1, 0, 0, 4)
            // to do the other walls this.placeWall(wallTexture, 5,1,1,0,0,4) find the numbers

            // GUN
            this.drawGun()

            // Ballons
            for (let index = 0; index < 10; index++) {
                this.drawBallons()
            }

            // text- time renderer
            this.timerDiv = document.createElement('div')
            this.timerDiv.id = 'timerDiv'
            this.timerDiv.textContent = 'time: 0'
            this.timerDiv.style.backgroundColor = ' transparent'
            this.timerDiv.style.fontSize = '30px'

            const timerLabel = new CSS2DObject(this.timerDiv)
            timerLabel.position.set(0, 0, 0)
            this.scene.add(timerLabel)
            timerLabel.layers.set(0)

            this.labelrenderer = new CSS2DRenderer()
            this.labelrenderer.setSize(window.innerWidth * 15 / 100, window.innerHeight * 10 / 100)
            this.labelrenderer.domElement.id = "labelrenderer"
            this.labelrenderer.domElement.style.position = "absolute"
            this.labelrenderer.domElement.style.left = "5%"
            this.labelrenderer.domElement.style.top = "10%"
            document.body.appendChild(this.labelrenderer.domElement)

            this.scoreDiv = document.createElement('div')
            this.scoreDiv.id = 'scoreDiv'
            this.scoreDiv.textContent = 'Score: 0'
            this.scoreDiv.style.backgroundColor = ' transparent'
            this.scoreDiv.style.fontSize = '30px'

            const scoreLabel = new CSS2DObject(this.scoreDiv)
            scoreLabel.position.set(0, 2.5, 0)
            this.scene.add(scoreLabel)
            scoreLabel.layers.set(0)

            // renderer setup
            this.renderer = new THREE.WebGLRenderer()
            this.renderer.setSize(window.innerWidth * 90 / 100, window.innerHeight * 90 / 100)
            this.renderer.domElement.id = "canvas"
            this.renderer.domElement.style.position = "absolute"
            this.renderer.domElement.style.left = "5%"
            this.renderer.domElement.style.right = "5%"
            this.renderer.domElement.style.top = "8%"
            document.body.appendChild(this.renderer.domElement)

            this.renderer.domElement.addEventListener('mousemove', this.mouseMove)
            this.renderer.domElement.addEventListener('click', this.mouseClick)

            this.animate()
        },
        animate() {
            requestAnimationFrame(this.animate)

            this.delta = this.clock.getDelta()
            // this.removeOldBullets();

            for (let index = 0; index < this.ballons.length; index++) {
                this.ballons[index].position.y += this.ballons[index].speed * this.delta

                if (this.ballons[index].position.y > 2.25 || this.ballons[index].position.y < 0) {
                    this.ballons[index].speed = this.ballons[index].speed * (-1)
                }

            }

            for (let index = 0; index < this.bullets.length; index++) {
                this.bullets[index].alive -= this.delta
                if (this.bullets[index].alive < 0) {
                    this.bullets[index].material.dispose()
                    this.bullets[index].geometry.dispose()
                    this.bullets[index].removeFromParent()
                    this.scene.remove(this.bullets[index])
                    this.bullets.splice(index, 1)
                    index -= 1
                }
            }

            for (let i = 0; i < this.bullets.length; i++) {
                this.bullets[i].position.set(
                    this.bullets[i].position.x + this.bullets[i].direction.x * this.delta * 2,
                    this.bullets[i].position.y + this.bullets[i].direction.y * this.delta * 2,
                    this.bullets[i].position.z + this.bullets[i].direction.z * this.delta * 2
                )


            }

            for (const object1 of this.bullets) {
                var i, j = 0
                for (const object2 of this.ballons) {
                    const boundingBox1 = new THREE.Box3().setFromObject(object1);
                    const boundingBox2 = new THREE.Box3().setFromObject(object2);

                    if (boundingBox1.intersectsBox(boundingBox2)) {
                        // Collision detected between object1 and object2
                        console.log("Collision detected between object1 and object2");

                        this.handleCollision(j, i)
                    }
                    j += 1
                }
                i += 1
            }



            this.renderer.render(this.scene, this.camera)
            this.labelrenderer.render(this.scene, this.camera)
        },

        handleCollision(balloonIndex, bulletIndex) {

            // this.scene.remove(this.loadedMesh[balloonIndex]);
            // this.loadedMesh[balloonIndex] = null; // Clear the reference


            // // Dispose of the loaded materials

            // this.loadedMaterials[balloonIndex].dispose();
            // this.loadedMaterials[balloonIndex] = null; // Clear the reference

            // // Remove the balloon from the scene
            // this.scene.remove(balloonMesh);

            // // Remove the balloon from the array
            // this.ballons.splice(balloonIndex, 1);

            // Dispose of the bullet and balloon's resources
            this.mesh.material.dispose()
            this.mesh.geometry.dispose()
            this.mesh.removeFromParent()

            // Remove the bullet and balloon from the scene
            this.scene.remove(this.bullets[bulletIndex]);

            // Remove the bullet and balloon from their respective arrays
            this.bullets.splice(bulletIndex, 1);

            // Update the game score or perform any other desired actions
            this.score = this.score + 1;
            console.log(this.score)

            // Add any visual effects or animations to indicate the collision
            // this.playCollisionEffect();
        },
        placeWall(texture, scaleX, scaleY, scaleZ, positionX, positionY, positionZ) {

            this.mesh = new THREE.Mesh(
                new THREE.BoxGeometry(scaleX, scaleY, scaleZ),
                new THREE.MeshPhongMaterial({
                    color: 0xffffff,
                    map: texture
                })
            )
            this.mesh.position.set(positionX, positionY, positionZ)
            this.mesh.receiveShadow = true
            this.mesh.castShadow = true

            this.scene.add(this.mesh)
        },
        drawGun() {
            const scene = this.scene
            const camera = this.camera
            const gun = this.gun
            var mtlloader = new MTLLoader()
            mtlloader.load('/uziGold.mtl', function (materials) {
                materials.preload()
                var objloader = new OBJLoader()
                objloader.setMaterials(materials)

                objloader.load('/uziGold.obj', function (mesh) {
                    mesh.scale.setScalar(10)
                    mesh.position.set(camera.position.x, camera.position.y - 0.5, camera.position.z - 0.5)
                    mesh.rotation.set(camera.rotation.x, camera.rotation.y - Math.PI, camera.rotation.z)

                    scene.add(mesh)
                    gun.push(mesh)
                    // TODO sth legat de eroare si de mutat this.render.domElement.addEventListener('click', this.mouseClick) cele 2 
                })
            })
        },
        mouseMove(event) {
            event.preventDefault()

            if (this.mouseX == -1 && this.mouseY == -1) {
                this.mouseX = event.clientX
                this.mouseY = event.clientY

            }
            var vec = new THREE.Vector3()
            var pos = new THREE.Vector3()

            vec.set(
                (event.clientX / window.innerWidth) * 2 - 1,
                -(event.clientY / window.innerHeight) * 2 + 1,
                0.5
            )
            vec.unproject(this.camera)
            vec.sub(this.camera.position).normalize()

            var distance = (-5 - this.camera.position.z) / vec.z
            pos.copy(this.camera.position).add(vec.multiplyScalar(distance))
            this.gun[0].lookAt(pos)
            this.direction = new THREE.Vector3(
                pos.x - this.gun[0].position.x,
                pos.y - this.gun[0].position.y + 0.15,
                pos.z - this.gun[0].position.z,)
            this.direction.normalize()


        },
        mouseClick(event) {
            if (event.button == 0) {
                this.createBullet()
            }
        },
        drawBallons() {
            const scene = this.scene
            const ballons = this.ballons
            const areBalloonsMoving = this.areBalloonsMoving
            const loadedMaterials = this.loadedMaterials
            const loadedMesh = this.loadedMesh

            var mtlloader = new MTLLoader()
            mtlloader.load('/Balloon.mtl', function (materials) {
                materials.preload()
                loadedMaterials.push(materials)

                var objloader = new OBJLoader()
                objloader.setMaterials(materials)

                objloader.load('/Balloon.obj', function (mesh) {
                    loadedMesh.push(mesh)
                    var min = 0.25
                    var max = 0.75
                    mesh.scale.setScalar(parseFloat(Math.random() * (max - min) + min))
                    var min1 = -1.75
                    var max1 = 1.75
                    mesh.position.x = parseFloat(Math.random() * (max1 - min1) + min1)
                    var min2 = -0.25
                    var max2 = 0
                    mesh.position.y = parseFloat(Math.random() * (max2 - min2) + min2)
                    var min3 = 1.5
                    var max3 = 3.5
                    mesh.position.z = parseFloat(Math.random() * (max3 - min3) + min3)
                    min = 0.1
                    max = 0.5
                    mesh.speed = parseFloat(Math.random() * (max - min) + min)

                    if (areBalloonsMoving == false) {
                        mesh.speed = 0
                    }

                    scene.add(mesh)
                    ballons.push(mesh)
                })
            })
        },
        removeOldBullets() {
            const newBullets = [];

            for (let i = 0; i < this.bullets.length; i++) {
                if (this.bullets[i].alive > 0) {
                    newBullets.push(this.bullets[i]);
                } else {
                    this.scene.remove(this.bullets[i]);
                    this.bullets[i].geometry.dispose();
                    this.bullets[i].material.dispose();
                }
            }

            this.bullets = newBullets;
        },

        createBullet() {
            this.mesh = new THREE.Mesh(
                new THREE.SphereGeometry(0.025, 6, 6),
                new THREE.MeshPhongMaterial({
                    color: 0xffffff
                })
            )
            this.mesh.position.set(
                this.gun[0].position.x,
                this.gun[0].position.y + 0.15,
                this.gun[0].position.z
            )
            this.mesh.receiveShadow = true
            this.mesh.castShadow = true
            this.mesh.direction = this.direction
            this.mesh.alive = 2

            // const bulletResource = {
            //     material: mesh.material,
            //     geometry: mesh.geometry
            // };
            // this.bulletResources.push(bulletResource);

            this.scene.add(this.mesh)
            this.bullets.push(this.mesh)

        },
        resize(event) {
            this.renderer.setSize(window.innerWidth * 15 / 100, window.innerHeight * 10 / 100)
            this.labelrenderer.setSize(window.innerWidth * 15 / 100, window.innerHeight * 10 / 100)
            this.camera.aspect = window.innerWidth / window.innerHeight
        },
        freezeGame() {
            this.gameFrozen = true;
            // Stop any animations or interactions here
            this.areBalloonsMoving = false;
        },

        restartGame() {
            this.gameFrozen = false;
            // Reset game state and restart animations here
            this.animate()
        },
        // return to main Menu
        mainMenu() {
            this.$emit("changeState", 2)
        },
        toScores() {
            this.$emit("changeState", 3)
        },
        SignIn() {
            this.$emit("changeState", 0)
        }
    }
}

</script>

<template>
    <v-toolbar style="position: absolute; top:0%; left: 0%; height: 7% ;">


        <button class="btn" type="button" @click="SignIn()">Log Out</button>
        <button class="btn" type="button" @click="mainMenu()">Back to Menu</button>
        <button class="btn" @click="toScores()">To the Highscores</button>

    </v-toolbar>
    <span v-text="this.title"></span>

    <v-container style=" position: absolute; left:5%;right: 5%; background-color: aliceblue; top:8%;">

        <!-- Your existing game content -->
        <div v-if="gameFrozen" class="overlay">
            <div class="overlay-content">
                <p>Game Paused</p>
                <button @click="restartGame">Restart</button>
            </div>
        </div>

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

/* Add styles for the overlay and its content */
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
}

.overlay-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
}

/* Add styles for the restart button */
.overlay button {
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}
</style>