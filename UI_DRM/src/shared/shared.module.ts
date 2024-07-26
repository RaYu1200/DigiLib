import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DropFileDirective } from './directive/drop-file.directive';
import { CardComponent } from './components/card/card.component';
import { AngularMaterialsModule } from './material.module';


@NgModule({
  declarations: [
    DropFileDirective,
    CardComponent
  ],
  imports: [
    CommonModule,
    AngularMaterialsModule
  ],
  exports : [
    DropFileDirective,
    CardComponent
  ]
})
export class SharedModule { }
