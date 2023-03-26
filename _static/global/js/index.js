import DiceBox from "https://cdn.jsdelivr.net/npm/@3d-dice/dice-box-threejs@0.0.12/dist/dice-box-threejs.es.min.js";

let x = js_vars.dice_number; // use the random number from oTree
let str = x.toString(); // Converts 5 to "5"
let outcome = "1d6@" + str; //the outcome

// console.log(outcome);

// set configurations when invoking the class
const Box = new DiceBox("#app", {
  theme_customColorset: {
    // background: [
    //   "#00ffcb",
    //   "#ff6600",
    //   "#1d66af",
    //   "#7028ed",
    //   "#c4c427",
    //   "#d81128"
    // ], // randomly assigned colors
    background: "#00ffcb",
    foreground: "#ffffff"
  },
  light_intensity: 1,
  gravity_multiplier: 600,
  baseScale: 70,
  strength: 2,
  onRollComplete: (results) => {
    console.log(`I've got results :>> `, results);
  }
});


Box.initialize()
  .then(() => {
    // give code sandbox a chance to load up
    setTimeout(() => {
      Box.roll("");
      // Box.roll("1d2+1d4+1d6+1d8+1d10+1d12+1d20+1d100");
    }, 300);
  })
  .catch((e) => console.error(e));

const rollBtn = document.getElementById("rollBtn");
rollBtn.addEventListener("click", () => {
  // // dynamically update the dice theme on each roll
  // const colors = [
  //   "#00ffcb",
  //   "#ff6600",
  //   "#1d66af",
  //   "#7028ed",
  //   "#c4c427",
  //   "#d81128"
  // ];
  // const randomColor = colors[Math.floor(Math.random() * colors.length)];

  // // all dice will produce the same value picked from the values list randomly
  // const values = [1, 2, 3, 4, 5, 6];
  // const randomVal = values[Math.floor(Math.random() * values.length)];

  // Box.updateConfig({
  //   theme_customColorset: {
  //     background: randomColor,
  //     foreground: "#ffffff"
  //   }
  // });
  Box.roll(outcome);
});
