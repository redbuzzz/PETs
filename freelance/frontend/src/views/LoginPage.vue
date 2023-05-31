<template>
    <div class="login-container">
        <h2>Войти в аккаунт</h2>
        <form class="login-form" @submit.prevent="submitForm">
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" v-model="username">
            <label for="password">Пароль:</label>
            <input type="password" id="password" v-model="password">
            <button type="submit">Войти</button>
        </form>
        <p>Еще нет аккаунта?
            <router-link to="/register">Зарегистрируйтесь</router-link>
        </p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: "",
            password: "",
        };
    },
    methods: {
        submitForm() {
            // здесь должна быть логика входа пользователя
        },
    },
};
</script>

<style>
.login-container {
    border: 2px solid black;
    padding: 20px;
    background-color: white;
    max-width: 400px;
    margin: 0 auto;
}

h2 {
    margin-top: 0;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

input[type="text"],
input[type="password"] {
    padding: 10px;
    border: none;
    border-bottom: 2px solid black;
}

button[type="submit"] {
    background-color: black;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
    background-color: gray;
}
</style>
