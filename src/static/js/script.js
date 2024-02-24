document.addEventListener("scroll", function () {
    let parallaxIntensity = window.innerWidth > 475 ? 0.08 : 0.04;
    const translateY = window.pageYOffset;
    document.body.style.setProperty('--scroll', `${-translateY * parallaxIntensity}px`);
});