function toggleNav() {
    const navContent = document.querySelector('.nav-content');
    navContent.classList.toggle('active');
  }
  

import { Carousel, initMDB } from "mdb-ui-kit";

initMDB({ Carousel });



function goToLoginPage() {
    console.log('goToLoginPage function called');
    window.location.href = '/login';
}

