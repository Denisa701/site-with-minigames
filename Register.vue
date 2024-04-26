<script>
import axios from 'axios';

export default {
    name: "Login",
    methods:
    {
        async mainMenu() {
            const username = document.getElementById("username").value
            const password = document.getElementById("password").value
            const email = document.getElementById("email").value
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);
            formData.append('email', email);

            // password verification and email check 

            if (document.getElementById("email").value && document.getElementById("password").value && document.getElementById("username").value) {
                if (document.getElementById("password").value == document.getElementById("passConfirm").value) {

                    const response = await axios.post('http://127.0.0.1:5000/register/',
                        formData,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        });

                    console.log(response.data.message);
                    if (response.data.message === "Succesful sign in") {
                        const result = await this.getuserID(username)
                        this.$emit("username", result);
                        this.$emit("changeState", 2);
                    } else {
                        document.getElementById("error").textContent = "Something went wrong "; // Corrected spelling
                        setTimeout(() => {
                            document.getElementById("error").textContent = "";
                        }, 2000);
                    }
                }
                else {
                    document.getElementById("error").textContent = "Password and password confirmation are not the same"
                    setTimeout(() => {
                        document.getElementById("error").textContent = ""
                    }, 2000)
                }
            }
            else {
                document.getElementById("error").textContent = " please fill all the fields"
                setTimeout(() => {
                    document.getElementById("error").textContent = ""
                }, 2000)
            }

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
        Login() {

            this.$emit("changeState", 0)

        }
    }
}
</script>

<template>
    <div>
        <h1>Create an account</h1>
        <label><b>Email:</b></label>
        <input type="text" placeholder="Enter email" id="email">
        <br>
        <label><b>Username:</b></label>
        <input type="text" placeholder="Enter username" id="username">
        <br>
        <label><b>Password:</b></label>
        <input type="password" placeholder="Enter password" id="password">
        <br>
        <label><b>Confirm password:</b></label>
        <input type="password" placeholder="Enter password" id="passConfirm">
        <br>
        <p id="error"></p>
        <button type="button" @click="mainMenu()">Register</button>
        <div type="button" @click="Login()">back to login page</div>
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