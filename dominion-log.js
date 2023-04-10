// ==UserScript==
// @name         Dominion deck tracker
// @namespace    https://ntsd.dev
// @version      0.1
// @description  track dominion players deck by log
// @author       ntsd
// @match        https://dominion.games*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=dominion.games
// @grant        none
// ==/UserScript==

const groupPlayer = 'player';
const groupAction = 'action';
const groupCount = 'count';
const groupCard = 'card';

const actionRegex = `(?<player>[A-Za-z ]+) (?<action>starts with|gains|trashes) (?<count>[0-9]+|a|an) (?<card>[A-Za-z\s]+).`;

const victoryScore = {
    'curse': -1,
    'estate': 1,
    'duchy': 3,
    'province': 6,
    'colony': 12,
}

const treasure = {
    'copper': 1,
    'silver': 2,
    'gold': 3,
    'platinum': 4,
};

const matchAll = (str, re) => {
    return [...str.matchAll(re)];
};

const parseCount = (str) => {
    if (str === 'a' || str === 'an') return 1;
    return parseInt(str);
}

const parseCard = (str) => {
    // remove plural
    if (str.at(-1) === 's') {
        str = str.slice(0, -1);
    }
    return str.toLowerCase();
}

const run = () => {
    const logContainer = document.getElementsByClassName('log-scroll-container')[0];
    const chatContainer = document.getElementsByClassName('chat-scroll-container')[0];

    let players = {};

    const actions = matchAll(logContainer.textContent, actionRegex);
    actions.forEach((matched) => {
        let player = matched.groups[groupPlayer];

        // the player suffic with ` buys and` when the action is `buy and gains`
        if (player.endsWith(' buys and')) {
            player = player.split(' buys and')[0]
        }

        // add player if not existing
        if (!players[player]) {
            players[player] = {
                cards: {},
                score: 0,
            };
        }

        const action = matched.groups[groupAction];
        let count = parseCount(matched.groups[groupCount]);
        const card = parseCard(matched.groups[groupCard]);

        // deduct if the action is `trashes`
        if (action === 'trashes') {
            count = -count;
        }

        // add card
        if (players[player].cards[card]) {
            players[player].cards[card] += count;
        } else {
            players[player].cards[card] = count;
        }

        // calculate score
        if (victoryScore[card]) {
            players[player].score += victoryScore[card] * count;
        }
    })

    chatContainer.innerHTML = ''

    for (const [name, player] of Object.entries(players)) {
        chatContainer.innerHTML += `
            <b>${name} (${player.score})</b>
            <br/>
            ${JSON.stringify(player.cards)}
            <br/>
        `;
    }

    return players;
}

(function () {
    'use strict';

    setInterval(function () {
        try {
            run();
        } catch (error) {
            console.error(error);
        }
    }, 5000);
})();
