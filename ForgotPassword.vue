<script>
import axios from 'axios'
export default {
    name: "forgotPass",
    methods:
    {
        async resetPass() {
            try {
                const email = document.getElementById("email").value; // .value is needed to get the input value
                var password = document.getElementById("password").value;
                console.log(email);
                console.log(password);

                const formData = new FormData();
                formData.append('email', email);
                formData.append('password', password);

                const response = await axios.put('http://127.0.0.1:5000/resetPass/',
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    });

                console.log(response.data.message);
                if (response.data.message === "password reseted succesfully") { // Check for strict equality (===)
                    this.$emit("changeState", 0);
                } else {
                    document.getElementById("error").textContent = "something went wrong"; // Corrected spelling
                    setTimeout(() => {
                        document.getElementById("error").textContent = "";
                    }, 2000);
                }
            } catch (error) {
                document.getElementById("error").textContent = "Eroare"; // Changed error message
                setTimeout(() => {
                    document.getElementById("error").textContent = "";
                }, 2000);
                console.error('Error:', error);
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

        },
    }
}
</script>

<template>
    <div>
        <h1>RESET PASSWORD</h1>
        <label><b>Email:</b></label>
        <input type="text" placeholder="Enter your mail" id="email">
        <br>
        <label><b>New password:</b></label>
        <input type="password" placeholder="Enter password" id="password">
        <br>
        <p id="error"></p>
        <button type="button" @click="resetPass()">Reset password</button>
        <div type="button" class="regBtn" @click="Login()">Register</div>
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