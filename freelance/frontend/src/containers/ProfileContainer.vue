<template>
  <div>
    <b-row>
      <b-col cols="1" md="8">
        <div>
          <b-jumbotron>
            <div v-if="!isHasProfile">
              <b-alert show>Создайте профиль, чтобы начать его редактировать</b-alert>
              <b-button @click="submitCreateProfile">Создать профиль</b-button>
            </div>
            <div v-if="success!==null || isSuccess!==null">
              <b-alert variant="success" show>{{ this.success || this.isSuccess }}</b-alert>
            </div>
            <div v-if="error!==null || isError!==null">
              <b-alert variant="danger" show>{{ this.error || this.isError }}</b-alert>
            </div>
            <template #header><p :class="isDark ? 'mb-2 color' : 'mb-2 color2'">Профиль</p></template>

            <template #lead>
              <p :class="isDark ? 'mb-2 color' : 'mb-2 color2'">Здесь вы можете изменить и добавить данные о себе</p>
            </template>

            <hr class="my-4" :style="isDark ? 'color: white;' : 'color: black'">
            <div v-if="isHasProfile">
              <b-form @submit.prevent="onSubmit">
                <b-form-group :class="isDark ? 'mb-2 color' : 'mb-2 color2'"
                              id="input-group-1"
                              label="Email address:"
                              label-for="input-1"
                              description="Будьте внимательнее!"

                >
                  <b-form-input class="mt-2"
                                id="input-1"
                                v-model="form.email"
                                type="email"
                                placeholder="Введите email"

                                @mouseenter="showPasswordInput = true"
                                @mouseleave="hidePasswordInput"
                  ></b-form-input>
                </b-form-group>

                <b-form-group v-if="showPasswordInput" :class="isDark ? 'mb-2 color' : 'mb-2 color2'"
                              id="input-group-password"
                              label="Password:"
                              label-for="input-password"
                >
                  <b-form-input class="mt-2"
                                id="input-password"
                                v-model="form.password"
                                type="password"
                                placeholder="Ведите пароль"

                  ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Ваше имя:" label-for="input-2"
                              :class="isDark ? 'mb-2 color' : 'mb-2 color2'">
                  <b-form-input class="mt-2"
                                id="input-2"
                                v-model="form.first_name"
                                placeholder="Введите имя"

                  ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="Ваша фамилия:" label-for="input-100"
                              :class="isDark ? 'mb-2 color' : 'mb-2 color2'">
                  <b-form-input class="mt-2"
                                id="input-100"
                                v-model="form.last_name"
                                placeholder="Введите фамилию"

                  ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="Город:" label-for="location"
                              :class="isDark ? 'mb-2 color' : 'mb-2 color2'">
                  <b-form-input class="mt-2"
                                id="location"
                                v-model="form.location"
                                placeholder="Введите город"

                  ></b-form-input>
                </b-form-group>
                <b-form-group id="input-group-2" label="Ваша дата рождения:" label-for="date"
                              :class="isDark ? 'mb-2 color' : 'mb-2 color2'">
                  <b-form-datepicker class="mt-2"
                                     id="date"
                                     v-model="form.birth_date"
                                     placeholder="Выберите дату"
                                     locale="ru"
                  ></b-form-datepicker>
                </b-form-group>
                <b-button type="submit" variant="primary">Обновить</b-button>
                <b-button type="reset" variant="danger">Сбросить</b-button>
              </b-form>
            </div>
          </b-jumbotron>
        </div>
      </b-col>
      <b-col cols="6" md="4" :class="isDark ? 'mt-4 color' : 'mt-4 color2'">
        <div class="mt-5">
          <b-alert variant="info" show>Выберите роль</b-alert>
          <b-alert variant="primary" show v-if="isFreelancer">Вы вошли как фрилансер</b-alert>
          <b-alert variant="primary" show v-if="isCustomer">Вы вошли как заказчик</b-alert>
          <b-button size="lg" class="button-margin" :variant="isDark ? 'dark' : 'light'" :pressed="isFreelancer"
                    @click="submitFreelance">Фрилансер
          </b-button>
          <b-button size="lg" class="button-margin" :variant="isDark ? 'dark' : 'light'" :pressed="isCustomer"
                    @click="submitCustomer">Заказчик
          </b-button>
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import {mapActions, mapState} from "pinia";
import {useProfileStore} from "@/stores/profileStore";
import {useAuthStore} from "@/stores/authStore";

export default {
  name: 'ProfileContainer',
  data() {
    return {
      form: {
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        location: '',
        birth_date: '',
      },
      showPasswordInput: false,
      hideTimeout: null
    }
  },
  async created() {
    await this.checkProfile();
    this.form.last_name = this.profileInfo?.last_name
    this.form.first_name = this.profileInfo?.first_name
    this.form.birth_date = this.profileInfo?.birth_date
    this.form.location = this.profileInfo?.location
  },
  methods: {
    async submitFreelance() {
      await this.chooseFreelancerRole();
    },
    async submitCustomer() {
      await this.chooseCustomerRole();
    },
    async onSubmit() {
      {
        if (this.form.email) {
          await this.updateProfileEmail(this.form.email, this.form.password);
        }
        await this.updateProfileWithoutEmail(this.form.last_name, this.form.first_name,
            this.form.birth_date, this.form.location)
      }
    },
    hidePasswordInput() {
      this.hideTimeout = setTimeout(() => {
        this.showPasswordInput = false;
      }, 45000);
    },
    async submitCreateProfile() {
      await this.createProfile();

    },
    ...mapActions(useProfileStore, ['checkProfile', 'createProfile', 'updateProfileEmail',
      'updateProfileWithoutEmail', 'chooseFreelancerRole', 'chooseCustomerRole'])
  },
  computed: {
    ...mapState(useProfileStore, ['isProfile', 'isHasProfile', 'profileInfo',
      'success', 'error', 'isSuccess', 'isError', 'isFreelancer', 'isCustomer']),
    ...mapState(useAuthStore, ['isDark']),
    FormattedBirthDate: {
      get() {
        if (this.form.birth_date instanceof Date) {
          const year = this.form.birth_date.getFullYear();
          const month = String(this.form.birth_date.getMonth() + 1).padStart(2, '0');
          const day = String(this.form.birth_date.getDate()).padStart(2, '0');
          return `${year}-${month}-${day}`;
        }
        return this.form.birth_date;
      },
      set(value) {
        if (value) {
          const [year, month, day] = value.split('-');
          this.form.birth_date = new Date(year, month - 1, day);
        } else {
          this.form.birth_date = '';
        }
      }
    }
  },

  beforeUnmount() {
    clearTimeout(this.hideTimeout);
  }
}
</script>


<style scoped>
.color {
  color: whitesmoke;
}

.color2 {
  color: black;
}

.button-margin {
  margin-right: 2%;
}
</style>
