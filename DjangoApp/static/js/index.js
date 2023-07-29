function onlySpaces(str)
{
    return str.trim().length === 0;
}

$(document).ready(function(){
    $("form").on("submit",function(event){
        
        var msg = $("#review").val();

        if(onlySpaces(msg)==false){
            document.getElementById("changer").setAttribute("hidden",false);
            document.getElementById("loading").removeAttribute("hidden");
            document.getElementById("resultdiv").setAttribute("hidden",false);
            $.ajax({
                data:{
                    res:msg,
                },
                type:"POST",
                url:"predict",
            }).done(function(data){

                // data = JSON.parse(data);
                // alert(data);

                var msg = data["message"];
                var name = data["movie_name"];
                // var imdb_rating = data["imdb_rating"]
                var review_rating = data["review_rating"]


                document.getElementById("loading").setAttribute("hidden",false);
                document.getElementById("resultdiv").removeAttribute("hidden");

                document.getElementById("details").innerHTML = "Movie Title: " + name + "<br>Review rating: " + review_rating;
                document.getElementById("result").innerHTML = msg;
                if (msg == "The movie is Good"){
                    document.getElementById("container").style.backgroundColor = "#64ff6433";
                }
                if (msg == "The movie is Neutral"){
                    document.getElementById("container").style.backgroundColor = "#9b86f9cc";
                }
                if (msg == "The movie is Bad"){
                    document.getElementById("container").style.backgroundColor = "#ff646499";
                }
            });
        }
        else{
            document.getElementById("resultdiv").setAttribute("hidden",false);
            document.getElementById("changer").removeAttribute("hidden");
            document.getElementById("container").style.backgroundColor = "#9b86f9cc";
        }
        event.preventDefault();
    });
});