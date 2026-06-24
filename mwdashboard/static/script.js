async function loadData(){

let response=await fetch("/status")

let data=await response.json()

let dashboard=document.getElementById("dashboard")

dashboard.innerHTML=""

for(let site in data){

let item=data[site]

dashboard.innerHTML+=`

<div class="card ${item.status==="ONLINE"?"online":"offline"}">

<h3>${site}</h3>

<p>Status : ${item.status}</p>

<p>HTTP : ${item.status_code}</p>

<p>Response : ${item.response_time} ms</p>

<p>Last Check : ${item.last_checked}</p>

<button onclick="removeSite('${site}')">

Remove

</button>

</div>

`
}

}

async function addSite(){

let url=document.getElementById("siteInput").value

await fetch("/add",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

url:url

})

})

loadData()
}

async function removeSite(url){

await fetch("/remove",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

url:url

})

})

loadData()
}

async function changeInterval(){

let minutes=document.getElementById("interval").value

await fetch("/interval",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

minutes:minutes

})

})
}

loadData()

setInterval(

loadData,

5000

)

function openModal(){

document.getElementById("websiteModal").style.display="flex"

document.getElementById("urlError").innerText=""

}

function closeModal(){

document.getElementById("websiteModal").style.display="none"

document.getElementById("websiteName").value=""

document.getElementById("websiteUrl").value=""

}

function validateUrl(url){

const regex=/^(https?:\/\/)([\w\-]+\.)+[\w\-]+(\/.*)?$/i

return regex.test(url)

}

async function submitWebsite(){

let name=document.getElementById("websiteName").value.trim()

let url=document.getElementById("websiteUrl").value.trim()

if(name===""){

alert("Enter website name")

return

}

if(!validateUrl(url)){

document.getElementById("urlError").innerText="Invalid URL"

return

}

await fetch("/add",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

name:name,

url:url

})

})

closeModal()

await loadData()

}
