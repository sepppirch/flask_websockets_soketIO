
//https://stackoverflow.com/questions/50508717/custom-elements-not-setting-getting-attributes



class mcRButton extends HTMLElement {


    constructor() {
    super();
    }

    connectedCallback() {
      let template = document.querySelector('#mcRB-template').content;
      this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
    
      let name_button = this.shadowRoot.querySelector("#name");
      let x_button = this.shadowRoot.querySelector("#x");
    
      name_button.textContent = this.getAttribute('name');
      name_button.style.background=this.getAttribute('color');//("background",);
      console.log('create: '+ this.getAttribute('id'));

      name_button.addEventListener('click', () => {
        console.log('select '+ this.getAttribute('id'));
        socket.emit('ex', {msg: this.getAttribute('name'), id: this.getAttribute('id'), fn: "rem_butt_clicked"});
      });
    
      x_button.addEventListener('click', () => {
          console.log('remove '+ this.getAttribute('id') + ' from '+ this.parentElement.getAttribute('id'));
          socket.emit('ex', {id: this.getAttribute('id'), parent: this.parentElement.getAttribute('id'), fn: "rem_butt_del"});
          //this.remove();
      });

    }

}

customElements.define('mc-rbutton', mcRButton);



class mcRDropDown extends HTMLElement {

  constructor() {
  super();

    //set dropdown value: 
    //dropdown.value = opt[1];
  }

  connectedCallback() {
 
    let template = document.querySelector('#mcDD-template').content;
    this.attachShadow({ mode: 'open' }).appendChild(template.cloneNode(true));
  
    let dropdown = this.shadowRoot.querySelector("#dropdown");
    //var opt =  this.getAttribute('opt').split(",");
    var opt = JSON.parse(this.getAttribute('opt'));
    //console.log(opt);
    opt.forEach(function(item, index, array) {
     dropdown.append(new Option(item));
    });
  
    dropdown.addEventListener('change', () => {
      console.log("changed");
      socket.emit('ex', {id: this.getAttribute('id'), opt: dropdown.options[dropdown.selectedIndex].text, fn: "sel"});
    });
  }
}

customElements.define('mc-dropdown', mcRDropDown);


























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