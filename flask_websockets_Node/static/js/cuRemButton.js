
class InputGene extends HTMLElement {


    constructor() {
    super();


    let template = document.querySelector('#gene-template').content;
      this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
    
      let name_button = this.shadowRoot.querySelector("#name");
      let x_button = this.shadowRoot.querySelector("#x");
    
      name_button.textContent = this.getAttribute('name');
      name_button.style.background=this.getAttribute('color');//("background",);
      console.log('create: '+ this.getAttribute('id'));
      name_button.addEventListener('click', () => {
      console.log('select '+ this.getAttribute('id'));
      });
    
      x_button.addEventListener('click', () => {
          console.log('remove '+ this.getAttribute('id') + ' from '+ this.parentElement.getAttribute('id'));
          this.remove();
      });


    }
}

customElements.define('gene-button', InputGene);

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
            result += characters.charAt(Math.floor(Math.random() * 
            charactersLength));
        }
    return result;
}