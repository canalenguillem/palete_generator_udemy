const form = document.querySelector("#form");
form.addEventListener("submit", function (e) {
  e.preventDefault();
  const prompt = form.elements.prompt.value;
  //enviar la petición al servidor con fetch
  fetch("/paleta", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      prompt: prompt,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const colors = data.colors;
      const container = document.querySelector(".container");
      container.textContent = "";
      console.log(colors);
      for (const color of colors) {
        const div = document.createElement("div");
        div.classList.add("color");
        div.style.backgroundColor = color;
        div.style.width = `calc(100%/ ${colors.length})`;

        //crear un span
        span = document.createElement("span");
        span.textContent = color;
        div.appendChild(span);

        container.appendChild(div);

        //agregar evento al click
        div.addEventListener("click", function () {
          navigator.clipboard.writeText(color);
        });
      }
    });
});
