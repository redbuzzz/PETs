<template>
    <div class="input-block">
        <label :for="id" class="input-label">
            {{ label }}
        </label>
        <input :type="type" :name="name" :required="required" class="input-field" :id="id"
               :placeholder="placeholder"
                :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)"/>
    </div>
</template>

<script>
export default {
    name: "InputBlock",
    props: {
        modelValue: String,
        name: String,
        id: {
            type: String,
            default: (props) => props.name
        },
        label: {
            type: String,
            default: (props) => props.name
        },
        type: {
            type: String,
            default: (props) => props.name
        },
        placeholder: {
            type: String,
            default: (props) => props.name
        },
        required: {
            type: String,
            default: true
        }
    },
    emits: ['update:modelValue']
}
</script>

<style scoped>
.input-label {
    font-style: normal;
    font-weight: 700;
    font-size: 30px;
    margin-bottom: 10px;
    color: #FFFFFF;
}

.input-block {
    margin: 30px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 1;
}

.input-field {

    font-style: normal;
    font-weight: 700;
    font-size: 24px;
    text-align: center;
    width: 100%;

    color: #000000;
    background: #D9D9D9;
}
</style>
