<script setup>
import { ref } from 'vue'
const props = defineProps(['fit'])
const emit = defineEmits(['formatted'])

const blob = ref('');
//possibly try having the button in this part of the component and then bubble up the submit event
//try having conditional rendering of the rest of the form location etc down here. 

function formatFit() {
    let high = null, mid = null, low = null, rig = null, service = null, slotIndex
    let tempArr = []

    let obj = blob.value.split("\n")
    console.log(obj)

    for (let i in obj)  {
        console.log(obj[i])
        obj[i] == "High Power Slots" ?  high = i : null
        obj[i] == "Medium Power Slots" ?  mid = i : null
        obj[i] == "Low Power Slots" ?  low = i : null
        obj[i] == "Rig Slots" ?  rig = i : null
        obj[i] == "Service Slots" ?  service = i : null
    }

    let finalobj ={
        High: [],
        Mid: [],
        Low: [],
        Rig: [],
        Service: []
    }

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

    let formatedFit = JSON.stringify(Object.assign({}, finalobj))
    console.log(formatedFit)
    emit('formatted', (JSON.parse(formatedFit)))
}
</script>

<template>
    <textarea v-model="blob" @input="formatFit"></textarea>
</template>