
function _(key){
    try {
        return MESSAGES[key] || key;
    } catch(e) {}
    return key;
}

