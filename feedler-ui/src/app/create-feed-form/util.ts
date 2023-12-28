import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function validUrlValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    try {
      new URL(control.value);
      return null;
    } catch (error) {
      return { invalidUrl: { value: control.value } };
    }
  };
}
