function getData(genre) {
    fetch(`/get-shows-by-genre/${genre}`)
        .then(response => response.json())
        .then(data => createElements(data))
        .catch(error => console.log(error))
}

//show the title, rating, year, genre, actor count
function createElements(data) {
    let elements = ``

    elements += `<tr> 
        <th>Title</th>
        <th>Rating</th>
        <th>Year</th>
        <th>Genre</th>
        <th>Actor count</th>
        </tr>`

    for (let element of data) {
        if (element.year < 2000) {
            elements += `
            <tr class="mouseover">
            `
        } else {

            elements += `
            <tr> 
        `
        }

        elements+=`
            <td>${element.title}</td>
            <td>${element.rating}</td>
            <td>${element.year}</td>
            <td>${element.name}</td>
            <td>${element.actor_count}</td>
            </tr>
        `
    }

    showElements(elements)

}


function showElements(elements) {
    let container = document.getElementById('container')
    container.innerHTML = elements
}


function init() {
    let genres = document.querySelectorAll('#genre')
    console.log(genres)
    for (let genre of genres) {
        genre.addEventListener("click", function (e) {
            let genre_name = e.currentTarget.innerText
            getData(genre_name)

        })

    }
}

init()
