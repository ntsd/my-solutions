function encryptX(numStr) {
    return "x"+"\u200B".repeat(parseInt(numStr)+1)+"\uFEFF";
}

function decryptX(string, pos) {
    let x = string.match(/x(\u200B)*\uFEFF/g) || [];
    const onlyNumString = string.replace(/[^0-9]/g, "");
    return onlyNumString.slice(0, pos) + x.map(x => x.match(/\u200B/g).length-1).join("") + onlyNumString.slice(pos);
}

const text = "112314141242331"
let encrypt = "";

for(let i=0; i < text.length; i++) {
    if(i>5 && i<12) {
        encrypt = encrypt.concat(encryptX(text[i])); //"\u200B"+"\u180E"+"\uFEFF"
    }
    else {
        encrypt = encrypt.concat(text[i]);
    }
}

console.log(encrypt)
const decrypt = decryptX(cardNumber.value, 6);
console.log(decrypt)