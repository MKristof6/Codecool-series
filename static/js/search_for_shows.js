function getData(letter){
    fetch(`/get-seasons/${letter}`)
        .then(response => response.json())
        .then(data => getElementsData(data))
        .catch(error => console.log(error))
}

function getElementsData(data){
    elements=``
    elements+=`
    <tr>
    <th>Tite</th>
</tr>
    `

    for(let element of data){
       elements+=`
      > <tr>
      <td class="table_data" >${element.title}</td>
    </tr>
       `
    }
    showElements(elements)
    linkToGoogle()
}

function showElements(elements){
    let container = document.getElementById('container')
    container.innerHTML=elements
}

function linkToGoogle(){
    let tableDatas = document.querySelectorAll('.table_data')
    for(tableData of tableDatas) {
        tableData.addEventListener("click", function (event) {
            let title = event.currentTarget
            if (confirm(`Do you want to Google ${title.innerText}`)) {
                window.open(`https://google.com/search?q=${title.innerText}`)
            } else {
                alert('You are a potato!')
            }

        })
    }
}

function init(){
    let searchLetter = document.getElementById('search_letter')
    searchLetter.addEventListener("input", function (){
        getData(searchLetter.value)
    })

}
init()
