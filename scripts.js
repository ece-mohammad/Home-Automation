function getUsers(module_id, module_type)
{
    var req = new XMLHttpRequest();

    req.onreadystatechange = function()
    {
        if(this.readyState==4 && this.status ==200)
        {
            var data = JSON.parse(this.responseText);

            var res = "<table><tr><th>Registered Users:</th></tr>";

            for(var user = 0; user < data.users.length; user++)
            {
                res += ("<tr><td>"+ data.users[user] + "</td></tr>");
            }

            res += "</table>";

            document.getElementById("resultTable").innerHTML = res;
        }
    }

    req.open("GET", "/modules/"+module_id+"/"+module_type+".json", true);

    req.send(null);
}

function getLog(module_id, module_type)
{
    var req = new XMLHttpRequest();

    req.onreadystatechange = function()
    {
        if(this.readyState==4 && this.status ==200)
        {
            var data = JSON.parse(this.responseText);

            var res = "<table><tr><th>Last 10 logs:</th></tr>";

            var max_lines = 0;

            if (data.access_log.length > 10)
            {
                max_lines = 10;
            }
            else
            {
                max_lines = data.access_log.length;
            }

            for(var user = 0; user < max_lines ; user++)
            {
                res += ("<tr><td>"+ data.access_log[ data.access_log.length - user - 1 ] + "</td></tr>");
            }

            res += "</table>";

            document.getElementById("resultTable").innerHTML = res;
        }
    }

    req.open("GET", "/modules/"+module_id+"/"+module_type+".json", true);

    req.send(null);
}