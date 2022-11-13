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
                url:"/predict",
            }).done(function(data){
                document.getElementById("loading").setAttribute("hidden",false);
                document.getElementById("resultdiv").removeAttribute("hidden");
                document.getElementById("result").innerHTML = data;
            });
        }
        else{
            document.getElementById("resultdiv").setAttribute("hidden",false);
            document.getElementById("changer").removeAttribute("hidden");
        }
        event.preventDefault();
    });
});