function getData(genre) {
    fetch(`/get-shows-by-genre/${genre}`)
        .then(response => response.json())
        .then(data => getGenreElements(data))
        .catch(error => console.log(error))
}


function getGenreElements(data){
    let elements=``

    elements+=`<tr>
<th>Title</th>
<th>Season count</th>
<th>Episode count</th>
</tr>`

    for(let element of data) {
        elements += `
    <tr>
    <td>${element.title}</td>
    <td>${element.season_count}</td>
    <td>${element.episode_count}</td>
    </tr>`
    }

    showElements(elements)

}

function showElements(elements) {
    let container = document.getElementById('container')
    container.innerHTML = elements
}
function init(){
    let select_btn = document.getElementById('select_button')
    select_btn.addEventListener("click", function (){
        let option=document.getElementById('genre_select')
        getData(option.value)
    })
}

init()
