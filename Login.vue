<script>
import axios from 'axios'
export default {
    name: "Login",
    methods:
    {
        async handleSubmit() {
            try {
                const username = document.getElementById("username").value; // .value is needed to get the input value
                var password = document.getElementById("password").value;
                console.log(username);
                console.log(password);

                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);

                const response = await axios.post('http://127.0.0.1:5000/login/',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });

                console.log(response.data.message);
                if (response.data.message === "Autentificare reușită") { // Check for strict equality (===)
                    const result = await this.getuserID(username)
                    this.$emit("username", result);
                    this.$emit("changeState", 2);
                } else {
                    document.getElementById("error").textContent = "Autentificare eșuată"; // Corrected spelling
                    setTimeout(() => {
                        document.getElementById("error").textContent = "";
                    }, 2000);
                }
            } catch (error) {
                document.getElementById("error").textContent = "Eroare la autentificare"; // Changed error message
                setTimeout(() => {
                    document.getElementById("error").textContent = "";
                }, 2000);
                console.error('Error:', error);
            }
        },
        register() {

            this.$emit("changeState", 1)

        },
        async getuserID(username) {
            const api = axios.create({
                baseURL: 'http://127.0.0.1:5000',
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                timeout: 10000
            })

            const response = await api.get('/getuserID/' + username)

            return response.data.result;

        },
        resetPass() {

            this.$emit("changeState", (-1))

        }
    }
}
</script>

<template>
    <div>
        <h1>Sing IN</h1>
        <label><b>Username:</b></label>
        <input type="text" placeholder="Enter username" id="username">
        <br>
        <label><b>Password:</b></label>
        <input type="password" placeholder="Enter password" id="password">
        <br>
        <p id="error"></p>
        <button type="button" @click="handleSubmit()">Login</button>
        <div type="button" class="regBtn" @click="register()">Register</div>
        <div type="button" class="regBtn" @click="resetPass()">Forgot the password?</div>
    </div>
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

.regBtn {
    color: rgba(0, 255, 68, 0.525);
    font-size: large;
}

input {
    width: 100%;
    padding: 12px 20px;
    margin: 10px;
    background-color: white;
}

#error {
    color: red;
    display: table;
    margin: 0 auto;
}
</style>