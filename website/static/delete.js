function deleterecipe(recipeId){
    fetch('/delete-recipe',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipeId: recipeId})
    }).then((_res) => {
        window.location.href = "/yourrecipe"
    })
    .catch(error => console.error("Error: ", error));
}