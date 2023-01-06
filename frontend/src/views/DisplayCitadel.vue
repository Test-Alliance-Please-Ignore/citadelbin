<script>
import CitadelFit from '@/components/CitadelFit.vue';
    export default {
    data() {
        return {
            searchVal: "",
            citResponse: "",
            isLoaded: false,
            submitter: "",
            fit: ""
        };
    },
    methods: {
        getCitadel() {
            let baseURL = "https://emdc8y90lc.execute-api.us-east-1.amazonaws.com/dev/citadels/";
            console.log(this.searchVal);
            let finalURL = baseURL.concat(this.searchVal);
            console.log(finalURL);
            this.axios.get(finalURL).then((response) => {
                console.log(response.data);
                this.citResponse = response.data; // 8/3 used to have index here [0]
                this.isLoaded = true;
            })
                .catch(function (error) {
                console.log(error);
            });
        },
        setFit(formatedFit) {
            this.fit = formatedFit
        },
        updateCitadel() {
            console.log("Button Clicked");
            let newPK = this.citResponse.PK;
            newPK = newPK.split("#")[1];
            console.log(newPK);
            // this still needs its fit formatted... 7/13
            let reqbody = { PK: newPK, SK: "", date: "", name: this.citResponse.name, system: this.citResponse.system, submitter: this.submitter, fitting: this.fit
            };
            console.log("REQ ", reqbody);
            
            this.axios.put('https://emdc8y90lc.execute-api.us-east-1.amazonaws.com/dev/citadel', reqbody)
            .then((response) => {
                console.log(response.data)
            })
            .catch(function (error) {
                console.log(error);
            })
            
        }
    },
    components: { CitadelFit }
}
</script>

<template>
    <div>
        <form @submit.prevent="getCitadel" class="bg-gray-100">
            <input v-model="searchVal" class= "bg-gray-200"/>
            <button type="submit" class="text-white bg-sky-900 hover:bg-lime-400"> SUBMIT</button>
        </form>
    </div>
    <div v-if="isLoaded">
        <h1 class="text-5xl">{{citResponse.PK}}</h1>
        <br>
        <h2 v-if="citResponse.fitting.High.length != 0" class="text-2xl">High</h2>
        <li v-for="item in citResponse.fitting.High">
            {{item}}
        </li>

        <h1 v-if="citResponse.fitting.Mid.length != 0" class="text-2xl">Mid</h1>
        <li v-for="item in citResponse.fitting.Mid">
            {{item}}
        </li>

        <h1 v-if="citResponse.fitting.Low.length != 0" class="text-2xl">Low</h1>
        <li v-for="item in citResponse.fitting.Low">
            {{item}}
        </li>

        <h1 v-if="citResponse.fitting.Rig.length != 0" class="text-2xl">Rig</h1>
        <li v-for="item in citResponse.fitting.Rig">
            {{item}}
        </li>

        <h1 v-if="citResponse.fitting.Service.length != 0" class="text-2xl">Service</h1>
        <li v-for="item in citResponse.fitting.Service">
            {{item}}
        </li>
    </div>
    

    
    <div id="UpdateForm">
        <form @sumbit.prevent class="bg-gray-100">
            <p>Submitter: </p>
            <input v-model="submitter" class="bg-gray-200"/>
            <p>Fit: </p>
            <CitadelFit @formatted="setFit"/>
            <button @click="updateCitadel" type="button" class="text-white bg-sky-900 hover:bg-lime-400"> SUBMIT</button>
        </form>

    </div>

</template>