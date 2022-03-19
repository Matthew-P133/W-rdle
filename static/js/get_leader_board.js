const url = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-score'

const renderTable = async (sort = 'score', index = 0) => {
    const baseUrl = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-'
    const response = await fetch(`${baseUrl}${sort}`, {method: "GET"})
    const defaultData = await response.json()
    // let defaultData
    // await $.get(`${baseUrl}${sort}`, (data, status) => {
    //     defaultData = data
    // })

    const table = document.getElementById('info-table')

    const flag = [null, null, null, null, null]
    const svgList = [null, null, null, null, null]
    const svgDefault = "/static/images/noun-sort-2269994.svg"
    const svgActive = "/static/images/noun-sort-2269990.svg"
    flag.forEach((value, flagIndex, array) => {
        if (flagIndex === index) {
            flag[flagIndex] = 'noun-sort-active'
            svgList[flagIndex] = svgActive
        } else {
            flag[flagIndex] = null
            svgList[flagIndex] = svgDefault
        }
    })

    const conditionList = ['score', 'games_won', 'games_lost', 'games_played', 'win_streak']
    const conditionContentList = ['Score', 'Games Won', 'Games Lost', 'Game Played', 'Win Streak']

    let th = ''
    conditionList.forEach((value, i, array) => {
        th += `<th onclick="sortedCondition('${conditionList[i]}', ${i})">${conditionContentList[i]}<embed src="${svgList[i]}" class="noun-sort ${flag[i]}"></th>`
    })

    table.innerHTML = `<thead>
        <tr>
          <th>Name</th>
          ${th}
        </tr>
        </thead>`

    const username = window.localStorage.getItem('user')

    let tempBody = ''
    for (const i of defaultData.data) {
        let target = ''
        if (i.name === username) {
            target = "(YOU)"
        }
        tempBody += `<tr>
            <th>${i.name}${target}</th>
            <th>${i.score}</th>
            <th>${i.games_won}</th>
            <th>${i.games_lost}</th>
            <th>${i.games_played}</th>
            <th>${i.win_streak}</th>
        </tr>`
        
    }


    table.innerHTML += `<tbody>${tempBody}</tbody>`
}
//render original table
renderTable()

const sortedCondition = (sort, index) => {
    renderTable(sort, index)
}