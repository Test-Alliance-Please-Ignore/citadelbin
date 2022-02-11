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
                const MyData = new FormData()
                MyData.append('first', this.message)
                MyData.append('second', this.mulMessage)
                console.log(MyData.entries)
                console.log(this.message)
                let date = new Date()
                console.log(date.toISOString())
                console.log(this.mulMessage)
                console.log(JSON.stringify(this.mulMessage))
                
                let obj = this.mulMessage.split("\n")
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