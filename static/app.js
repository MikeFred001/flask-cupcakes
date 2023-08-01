"use strict";

const BASE_URL = "http://localhost:5001/api/cupcakes";
const DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake";

const $cupcakeList = $('#cupcake-list');

function displayCupcakes(cupcakes) {
  $cupcakeList.empty();

  for (const cupcake of cupcakes) {
    const $cupcake = $(`
      <div>
        <img src="${cupcake.imageURL}">
        <p>Flavor: ${cupcake.flavor}</p>
        <p>Size: ${cupcake.size}</p>
        <p>Rating: ${cupcake.rating}</p>
      </div>
    `);

    $cupcakeList.append($cupcake);
  }
}

async function getCupcakes() {
  const resp = await axios({
    url: BASE_URL,
    method: "GET"
  });

  const cupcakes = resp.data.cupcakes;
  console.log(cupcakes);

  const cupcakeArr = cupcakes.map(cupcake => {
    console.log(cupcake);
    return {
      id: cupcake.id,
      flavor: cupcake.flavor,
      size: cupcake.size,
      rating: cupcake.rating,
      imageURL: cupcake.image_url || BASE_IMAGE_URL
    }
  });

  return cupcakeArr;
}

async function getAndDisplayCupcakes() {
  const cupcakes = await getCupcakes();
  const cupcakeHtml = displayCupcakes(cupcakes);
}

