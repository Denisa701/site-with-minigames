function mainMenu()
{
    if(document.getElementById("username").value && document.getElementById("password").value)
    {

        document.location.assign("menu.html");
    }
    else{
        document.getElementById("error").textContent = " please fill all the fields"
        setTimeout(()=>{
            document.getElementById("error").textContent = ""
        }, 2000)
    }

}

function highScores(game)
{
    document.location.assign(highScores.html)
}