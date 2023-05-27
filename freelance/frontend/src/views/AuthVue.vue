<template>
  <!--    логика Логина-->
    <div class="auth-card" >
        <div v-if="activeTab">
            <p class="error">{{ error }}</p>
            <h2 class="auth-card__title">Войти</h2>
            <form class="auth-form" @submit.prevent="submit">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" v-model="form.email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Пароль</label>
                    <input type="password" v-model="form.password" id="password" name="password" required>
                </div>
                <button type="submit">Войти</button>
            </form>
            <p class="auth-card__toggle" @click="toggleRegister">Нет аккаунта? Зарегистрироваться</p>
        </div>
        <!--        логика Регистрации-->
        <div v-if="!activeTab">
            <p class="error">{{error}}</p>
            <p v-if="success" style="color: whitesmoke">Вы успешно зарегистрировались!
            Подтвердите аккаунт на почте.</p>
            <h2 class="auth-card__title">Регистрация</h2>
            <form class="auth-form" @submit.prevent="submitRegistr">
                <div class="form-group">
                    <label for="email">E-mail</label>
                    <input type="email" id="email" v-model="form.email" required>
                </div>
                <div class="form-group">
                    <label for="password">Пароль</label>
                    <input type="password" id="password" v-model="form.password" required>
                </div>
                <button type="submit">Зарегистрироваться</button>
                <p class="auth-card__toggle" @click="toggleLogin">Есть аккаунт? Войти</p>
            </form>
        </div>
    </div>

</template>

<script>


import {mapActions, mapState} from "pinia";
import {useAuthStore} from "@/stores/authStore";
import {nextTick} from "vue";

export default {
    data() {
        return {
            isLogin: true,
            form: {
                email: "",
                password: null
            },

        }
    },
    methods: {
        ...mapActions(useAuthStore, ['setFalse', 'setTrue', 'login', 'register', 'createProfile']),
        async toggleRegister() {
            await this.setFalse();
        },
        async toggleLogin() {
            await this.setTrue();
        },
        async submit() {
            await this.login(this.form.email, this.form.password);
            await nextTick();
            if (this.isAuth) {
                this.$router.push({name: 'home'});
            } else {
                console.error(this.error);
            }
        },
        async submitRegistr () {
            await this.register(this.form.email, this.form.password);
            await this.createProfile();
            this.$router.push({name: 'login'});
        },

    },
    computed: {
        ...mapState(useAuthStore, ['activeTab', 'isAuth', 'error', 'success']),
    },

}
</script>

<style>

.auth-card {
    background-color: #333;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    width: 400px;
    margin: 12% auto 0;
}

.auth-card__title {
    color: #fff;
    font-size: 24px;
    margin-bottom: 20px;
}

.auth-form .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
}

.auth-form label {
    font-size: 18px;
    margin-bottom: 5px;
}

.auth-form input {
    padding: 10px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    background-color: #f5f5f5;
    transition: all 0.2s ease-in-out;
}

.auth-form input:focus {
    outline: none;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
}

.auth-form button {
    padding: 10px;
    font-size: 18px;
    color: #fff;
    background-color: #333;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}

.auth-form button:hover {
    background-color: #222;
}

.auth-card__toggle {
    color: #fff;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
}

.form-group label {
    color: white;
}

.auth-card {
    margin-top: 12%;
}

.error {
    color: red;
}

/* Адаптивность для устройств с максимальной шириной экрана 767px и меньше */
@media (max-width: 767px) {
    .auth-card {
        width: 70%;
        margin-top: 40%;
    }
}

/* Адаптивность для устройств с шириной экрана от 768px до 1023px */
@media (min-width: 768px) and (max-width: 1023px) {
    .auth-card {
        width: 50%;
        margin-top: 8%;
    }
}

/* Адаптивность для устройств с шириной экрана от 1024px и больше */
@media (min-width: 1024px) {
    .auth-card {
        width: 20%;
        margin-top: 12%;
    }
}


</style>
