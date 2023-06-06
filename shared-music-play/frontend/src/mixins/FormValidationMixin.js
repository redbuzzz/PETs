import _ from "lodash";
import useVuelidate from "@vuelidate/core";

export default {
  data() {
    return {
      form: {},
      v$: useVuelidate()
    }
  },
  validations: {
    form: {}
  },
  methods: {
    getErrorsByFieldName(fieldName) {
      let serverErrors;
      if (this.error && this.error.data && fieldName in this.error.data) {
        serverErrors = this.error.data[fieldName]
      } else {
        serverErrors = []
      }
      let frontErrors = (this.v$.form[fieldName].$error) ? this.v$.form[fieldName].$errors.map(e => e.$message) : [];
      return _.merge(frontErrors, serverErrors)
    },
  },
  computed: {
    error() {
      return null
    },
    fieldErrors() {
      let fieldErrors = {};
      for (let field in this.form) {
        fieldErrors[field] = this.getErrorsByFieldName(field)
      }
      return fieldErrors
    },
  },
}
