const path = require('path')
const fs = require('fs')

function getTerms() {
    let termsPath = path.join(__dirname, 'terms.json')
    return JSON.parse(fs.readFileSync(termsPath, 'utf-8'))
}

exports.getTerms = getTerms