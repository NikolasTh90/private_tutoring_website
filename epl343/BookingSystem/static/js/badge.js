const badge = document.querySelector('.badge-base')
let window_width = window.innerWidth
if (window_width <= 360)
    badge.style.marginLeft = '-40px'
else if(window_width <= 380)
    badge.style.marginLeft = '-30px'
else if (window_width <= 390)
    badge.style.marginLeft = '-20px'


const title = document.querySelector('#navbar-title')
if (window_width <= 990) {
    title.style.fontSize = "0px"
}