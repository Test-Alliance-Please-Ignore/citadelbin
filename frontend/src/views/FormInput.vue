<script>import axios from "axios";

    export default {
        data() {
            return {
                citName: '',
                system: '',
                submitter: '',
                mulMessage: '',
            };
        },
        methods: {
            onSubmit() {
                let high = null, mid = null, low = null, rig = null, service = null, slotIndex
                let tempArr = []
                //********** use MyData.get() to get the key of a fitting and then mess with the keys from there? Look up changing key names and then go from there */
                console.log("***************************")

                console.log(this.citName)
                let date = new Date()
                console.log(date.toISOString())
                
                let obj = this.mulMessage.split("\n")
                console.log(obj)
                console.log(JSON.stringify(obj))

                
                console.log("***************************")
                for (let i in obj)  {
                    console.log(obj[i])
                    obj[i] == "High Power Slots" ?  high = i : null
                    obj[i] == "Medium Power Slots" ?  mid = i : null
                    obj[i] == "Low Power Slots" ?  low = i : null
                    obj[i] == "Rig Slots" ?  rig = i : null
                    obj[i] == "Service Slots" ?  service = i : null
                }
                console.log(high, mid, low, rig, service)

                let finalobj ={
                    High: [],
                    Mid: [],
                    Low: [],
                    Rig: [],
                    Service: []
                }
                
                console.log(high, mid, low, rig, service)

                //this is still sending everything into service and skipping rig even though its there. Seems like values are getting initialized when doing the ++ 
                // looks like stuff near the end is just fine or if there is just a gap of one but missing the ending values breaks
                // maybe try grabbing the whole array from x slot point down then purge anything below any other slot name mention eg High- all purge starting with the next "slot" etc

                // use just the ++INDEX then do a quick search for anything saying slot and make the obj a slice from start to the slot tag
                if(high !== null) {
                    high++
                    tempArr = []
                    tempArr = (obj.slice(high))
                    console.log("tempppppp", tempArr)
                    slotIndex = tempArr.findIndex(ele => {
                        if(ele.includes("Slot")) {
                            return true
                        }
                    })
                    console.log("slotIndex", slotIndex)

                    if(slotIndex !== -1) {
                        finalobj.High = tempArr.slice(0, slotIndex)
                    } else {
                         finalobj.High = tempArr
                    }
                }

                if(mid !== null) {
                    mid++
                    tempArr = []
                    tempArr = (obj.slice(mid))
                    slotIndex = tempArr.findIndex(ele => {
                        if(ele.includes("Slot")) {
                            return true
                        }
                    })

                    if(slotIndex !== -1) {
                        finalobj.Mid = tempArr.slice(0, slotIndex)
                    } else {
                        finalobj.Mid = tempArr
                    }
                }

                if(low !== null) {
                    low++
                    tempArr = []
                    tempArr = (obj.slice(low))
                    slotIndex = tempArr.findIndex(ele => {
                        if(ele.includes("Slot")) {
                            return true
                        }
                    })

                    if(slotIndex !== -1) {
                        finalobj.Low = tempArr.slice(0, slotIndex)
                    } else {
                        finalobj.Low = tempArr
                    }
                }

                if(rig !== null) {
                    rig++
                    tempArr = []
                    tempArr = (obj.slice(rig))
                    slotIndex = tempArr.findIndex(ele => {
                        if(ele.includes("Slot")) {
                            return true
                        }
                    })

                    if(slotIndex !== -1) {
                        finalobj.Rig = tempArr.slice(0, slotIndex)
                    } else {
                        finalobj.Rig = tempArr
                    }
                }

                console.log("BLLLLALALDLLADLFKJDFLKJDAKFKJ", service)
                if(service !== null) {
                    service++
                    tempArr = []
                    tempArr = (obj.slice(service))
                    slotIndex = tempArr.findIndex(ele => {
                        if(ele.includes("Slot")) {
                            return true
                        }
                    })

                    if(slotIndex !== -1) {
                        finalobj.Service = tempArr.slice(0, slotIndex)
                    } else {
                         finalobj.Service = tempArr
                    }
                    
                }
                

                console.log(high, mid, low, rig, service)
                


                let testObj = JSON.stringify(Object.assign({}, finalobj)) //7/29 add?
                console.log("Testing assign: ", testObj)

                


                console.log("Before cull", finalobj)
                
                console.log(" Final Output ")
                console.log(testObj)
                this.PostFit(JSON.parse(testObj))

                //send POST to create citadel with Metadata tag, return its UUID and then post to add the fit?
                    
            },

            PostFit(fit) {

                let reqbody = {PK: this.citName,
                    SK: '',
                    date: '',
                    name: this.citName,
                    system: this.system,
                    submitter: this.submitter,
                    fitting: fit
                    }
                    console.log("REQ ", reqbody)
                
                this.axios.post('https://emdc8y90lc.execute-api.us-east-1.amazonaws.com/dev/citadel', reqbody)
                //dev https://emdc8y90lc.execute-api.us-east-1.amazonaws.com/dev/citadel
                //dev2 https://b96rhqjpdh.execute-api.us-east-1.amazonaws.com/dev2/citadel
                .then((response) => {
                    console.log(response.data)
                })
                .catch(function (error) {
                    console.log(error);
                })
                
            }
        }

    }
</script>

<template>
    <div id="Testing input" class="text-left">
        <form @submit.prevent="onSubmit" class="bg-gray-100"> 
            <p>Submitter: </p>
            <input v-model="submitter" class="bg-gray-200"/>
            <p>Name: </p>
            <input v-model="citName" class= "bg-gray-200"/>
            <br/>
            <p>Location:</p>
            <input v-model="system" class= "bg-gray-200"/>
            <p>Fit:</p>
            <textarea v-model="mulMessage" class="bg-sky-400"></textarea>
            <br/>
            <button type="submit" class="text-white bg-sky-900 hover:bg-lime-400"> SUBMIT</button>

        </form>
        
    </div>
</template>