import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { BackendApiService } from './backend-api.service';

import {FormsModule, ReactiveFormsModule} from '@angular/forms'
import {MatInputModule} from '@angular/material/input';
import {MatTableModule} from '@angular/material/table';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'

import { MatSliderModule } from '@angular/material/slider';
import { WorldcatListComponent } from './worldcat-list/worldcat-list.component';

@NgModule({
  declarations: [
    AppComponent,
    WorldcatListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatTableModule,
    // DemoMaterialModule,
    BrowserAnimationsModule,
    MatSliderModule,
  ],
  bootstrap: [AppComponent],
  providers: [BackendApiService]
})
export class AppModule { }
