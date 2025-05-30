
import { createVuetify } from 'vuetify';
import { VCalendar } from 'vuetify/labs/VCalendar';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';


import 'vuetify/styles';

import '@mdi/font/css/materialdesignicons.css';

export default createVuetify({
  components: {
    ...components,
    VCalendar,
  },
  directives,
  theme: {
    defaultTheme: 'light', 
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1976D2', 
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
          
        }
      },
      
    }
  },
  defaults: {
    VBtn: {
      
    },
    VTextField: {
      variant: 'outlined', 
    },
    VCard: {
      elevation: 2, 
    }
  },
  icons: {
    defaultSet: 'mdi', 
  },
});