<script>
    export default {
        data() {
            return {
                message: '',
                mulMessage: '',
            };
        },
        methods: {
            onSubmit() {
                //https://stackoverflow.com/questions/41431322/how-to-convert-formdata-html5-object-to-json
                const MyData = new FormData()
                MyData.append('first', this.message)
                MyData.append('second', this.mulMessage)
                for (let value of MyData.entries()) {
                    console.log(value)
                }
                //********** use MyData.get() to get the key of a fitting and then mess with the keys from there? Look up changing key names and then go from there */
                console.log("***************************")

                console.log(this.message)
                let date = new Date()
                console.log(date.toISOString())
                console.log(this.mulMessage)
                console.log(JSON.stringify(this.mulMessage))
                
                let obj = this.mulMessage.split("\n")
                console.log(obj) // this is already a JSON object here with 0 -> x being the keys? Not really Parse does not work
                console.log(JSON.stringify(obj))
            }
        }

    }

</script>

<template>
    <div id="Testing input" class="text-left">
        <form @submit.prevent="onSubmit" class="bg-gray-100"> 

            <input v-model="message" class= "bg-gray-200"/>
            <p> Message: {{message}}</p>
            <span> MultiLine {{mulMessage}}</span>
            <br/>
            <textarea v-model="mulMessage" class="bg-sky-400"></textarea>
            <br/>
            <button type="submit" class="text-white bg-sky-900 hover:bg-lime-400"> SUBMIT</button>

        </form>
        
    </div>
</template>