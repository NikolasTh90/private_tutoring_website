const switchers = [...document.querySelectorAll('.switcher')]

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
})

const form = document.querySelector('.forms-section')
let window_width = window.innerWidth
if (window_width <= 990)
    form.style.marginTop = '20px'
else
    form.style.marginTop = '120px'