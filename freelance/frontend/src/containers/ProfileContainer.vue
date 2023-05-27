<template>
  <b-row>
    <b-col cols="1" md="8">
      <div>
        <b-jumbotron>
          <div v-if="!isHasProfile">
            <b-alert show>Создайте профиль, чтобы начать его редактировать</b-alert>
            <b-button @click="submitCreateProfile">Создать профиль</b-button>
          </div>
          <div v-if="success!==null">
            <b-alert variant="success" show>{{ this.success }}</b-alert>
          </div>
          <div v-if="error!==null">
            <b-alert variant="danger" show>{{ this.error }}</b-alert>
          </div>
          <template #header>Профиль</template>

          <template #lead>
            Здесь вы можете изменить и добавить данные о себе
          </template>

          <hr class="my-4">
          <div v-if="isHasProfile">
            <b-form @submit.prevent="onSubmit">
              <b-form-group class="mb-2"
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

              <b-form-group v-if="showPasswordInput" class="mb-2"
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

              <b-form-group id="input-group-2" label="Ваше имя:" label-for="input-2" class="mb-2">
                <b-form-input class="mt-2"
                              id="input-2"
                              v-model="form.first_name"
                              placeholder="Введите имя"

                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-2" label="Ваша фамилия:" label-for="input-100" class="mb-2">
                <b-form-input class="mt-2"
                              id="input-100"
                              v-model="form.last_name"
                              placeholder="Введите фамилию"

                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-2" label="Город:" label-for="location" class="mb-2">
                <b-form-input class="mt-2"
                              id="location"
                              v-model="form.location"
                              placeholder="Введите город"

                ></b-form-input>
              </b-form-group>
              <b-form-group id="input-group-2" label="Ваша дата рождения:" label-for="date" class="mb-2">
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
    <b-col cols="6" md="4">Вы можете выбрать свою роль здесь
    </b-col>
  </b-row>
</template>

<script>
import {mapActions, mapState} from "pinia";
import {useProfileStore} from "@/stores/profileStore";

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
      'updateProfileWithoutEmail'])
  },
  computed: {
    ...mapState(useProfileStore, ['isProfile', 'isHasProfile', 'profileInfo', 'success', 'error']),
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
</style>
