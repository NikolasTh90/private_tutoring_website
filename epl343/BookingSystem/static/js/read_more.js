const parentContainer = document.querySelector('.read-more-btn')
parentContainer.addEventListener('click', event => {
    const current = event.target

    const isReadMorebtn = current.className.includes('read-more-btn')
    if (!isReadMorebtn)
        return;
    const currentText = event.target.parentNode.querySelector('.read-more-text')
    currentText.classList.toggle('read-more-text--show')

    current.textContent = current.textContent.includes('Read More...') ? "Read Less... " : "Read More... "
    if (current.textContent.includes('Read More...'))
        currentText.style.display = 'none'
    else
        currentText.style.display = 'inherit'
  
})