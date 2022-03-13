const url = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-score'
const renderTable = async (url) => {
    const response = await fetch(url, {method: "GET"})
    const defaultData = await response.json()
    console.log("defaultData", defaultData)
    const table = document.getElementById('info-table')
    table.innerHTML = `<thead>
            <th>Name</th>
            <th onclick="sortedScore()">Score</th>
            <th onclick="sortedGameWon()">Games Won</th>
            <th onclick="sortedGameLost()">Games Lost</th>
            <th onclick="sortedGamePlayed()">Game Played</th>
            <th onclick="sortedWinStreak()">Win Streak</th>
        </thead>`

    for (const i of defaultData.data) {
        console.log('i', i)
        table.innerHTML += `<tr>
            <th>${i.name}</th>
            <th>${i.score}</th>
            <th>${i.games_won}</th>
            <th>${i.games_lost}</th>
            <th>${i.games_played}</th>
            <th>${i.win_streak}</th>
        </tr>`
    }
}
//render original table
renderTable(url)

const sortedScore = () => {
    const url1 = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-score'
    renderTable(url1)
}

const sortedGameWon = () => {
    const url2 = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-games_won'
    renderTable(url2)
}
const sortedGameLost = () => {
    const url3 = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-games_lost'
    renderTable(url3)
}
const sortedGamePlayed = () => {
    const url4 = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-games_played'
    renderTable(url4)
}
const sortedWinStreak = () => {
    const url5 = 'http://127.0.0.1:8000/wordgame/get-leader-board/?sort=-win_streak'
    renderTable(url5)
}