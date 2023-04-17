searchField = document.querySelector('#searchField')
tableOutput = document.querySelector('.table-output')
tableBody = document.querySelector('.table-body')
appTable = document.querySelector('.app-table')
paginationContainer = document.querySelector('.pagination-container')
tableOutput.style.display = 'none'

searchField.addEventListener('keyup', (e) =>{

    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        fetch('search-expenses/', {
            body: JSON.stringify({ searchText: searchValue }),
            method: 'POST',
        }).then(res=>res.json()).then(data => {
            tableBody.innerHTML = ""
            console.log("data", data)
            tableOutput.style.display = 'block'
            appTable.style.display = 'none'
            paginationContainer.style.display = 'none'
            if(data.length===0){
                tableOutput.innerHTML = "No results found"
            }else{
                data.forEach((item)=>{
                    tableBody.innerHTML += `
                    <tr>
                        <td>${ item.amount }</td>
                        <td>${ item.category }</td>
                        <td>${ item.description }</td>
                        <td>${ item.date }</td>
                    </tr>`;
                })
            }
        });
    }else{
        tableOutput.style.display = 'none'
        appTable.style.display = 'block'
        paginationContainer.style.display = 'block'
    }
})