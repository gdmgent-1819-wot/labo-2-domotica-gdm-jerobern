(function () {

    const app = {
        init: function () {
            console.log("Initializing application");
            firebase.initializeApp(firebaseConfig);
            this.loadLights();
            this.loadOutlets();
            this.loadDoors();
            this.loadAlarm();
        },

        loadLights: function () {
            console.log("Loading lights");
            const lightsContainer = document.querySelector('.lights-container');
            firebase.database().ref('active_room/lights').on('value', snapshot => {
                lightsContainer.innerHTML = ''
                const lights = snapshot.val();
                // Render each light in the DOM
                for (let i = 0; i < lights.length; i++) {
                    let btnText = lights[i].is_on ? "On" : "Off";
                    let btnClass = lights[i].is_on ? "btn-warning" : "btn-outline-warning";
                    let status = lights[i].is_on ? "true" : "false";
                    lightsContainer.innerHTML += `
                    <div class="form-group form-row">
                        <label for="lightBtn${i}" class="col-sm-6 col-form-label">Light ${i + 1}</label>
                        <div class="col-sm-6">
                            <button data-id="${lights[i].id}" data-type="lights" data-status="${status}" type="button" class="light btn btn-block ${btnClass}" id="lightBtn${i}">${btnText}</button>
                        </div>
                    </div>
                    `
                }
                this.addEventListeners('.light');
            });
        },

        loadOutlets: function () {
            console.log("Loading Outlets");
            const outletsContainer = document.querySelector('.outlets-container');
            firebase.database().ref('active_room/outlets').on('value', snapshot => {
                outletsContainer.innerHTML = ''
                const outlets = snapshot.val();
                // Render each light in the DOM
                for (let i = 0; i < outlets.length; i++) {
                    let btnText = outlets[i].is_on ? "On" : "Off";
                    let btnClass = outlets[i].is_on ? "btn-primary" : "btn-outline-primary";
                    let status = outlets[i].is_on ? "true" : "false";
                    outletsContainer.innerHTML += `
                    <div class="form-group form-row">
                        <label for="outletBtn${i}" class="col-sm-6 col-form-label">Outlet ${i + 1}</label>
                        <div class="col-sm-6">
                            <button data-id="${outlets[i].id}" data-type="outlets" data-status="${status}" type="button" class="outlet btn btn-block ${btnClass}" id="outletBtn${i}">${btnText}</button>
                        </div>
                    </div>
                    `
                }
                this.addEventListeners('.outlet');
            });
        },

        loadDoors: function () {
            console.log("Loading Doors");
            const doorsContainer = document.querySelector('.doors-container');
            firebase.database().ref('active_room/doors').on('value', snapshot => {
                doorsContainer.innerHTML = ''
                const doors = snapshot.val();
                // Render each light in the DOM
                for (let i = 0; i < doors.length; i++) {
                    let btnText = doors[i].is_open ? "Open" : "Closed";
                    let btnClass = doors[i].is_open ? "btn-success" : "btn-danger";
                    let status = doors[i].is_open ? "true" : "false";
                    doorsContainer.innerHTML += `
                    <div class="form-group form-row">
                        <label for="doorBtn${i}" class="col-sm-6 col-form-label">Door ${i + 1}</label>
                        <div class="col-sm-6">
                            <button data-id="${doors[i].id}" data-type="doors" data-status="${status}" type="button" class="door btn btn-block ${btnClass}" id="doorBtn${i}">${btnText}</button>
                        </div>
                    </div>
                    `
                }
                this.addEventListeners('.door');
            });
        },

        loadAlarm: function () {
            const alarmBtn = document.getElementById('alarmBtn');
            firebase.database().ref('active_room/alarm').on('value', snapshot => {
                btnText = snapshot.val() ? 'Alarm On' : 'Alarm Off';
                alarmBtn.innerHTML = btnText;

            })
            alarmBtn.addEventListener('click', () => {
                // Change true to false or false to true in database
                firebase.database().ref('active_room/alarm').once('value').then(snapshot => {
                    value = snapshot.val() ? false : true;
                    firebase.database().ref('active_room/alarm').set(value);
                })
            })
        },

        addEventListeners: function (type) {
            let buttons = document.querySelectorAll(type);
            for (let i = 0; i < buttons.length; i++) {
                buttons[i].addEventListener('click', () => {
                    this.updateStatus(buttons[i].dataset.id, buttons[i].dataset.type, buttons[i].dataset.status);
                })
            }
        },

        updateStatus: function (id, type, status) {
            let key = (type == 'doors') ? 'is_open' : 'is_on';
            let value = (status === 'true') ? false : true;
            firebase.database().ref(`active_room/${type}/${id}/${key}`).set(value);
        }
    }
    app.init();
})();