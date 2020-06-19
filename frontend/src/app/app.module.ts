import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent, DialogOverviewExampleDialogComponent } from './app.component';
import {MatDialogModule} from '@angular/material/dialog';
import { HttpClientModule } from '@angular/common/http';
import { BackendApiService } from './backend-api.service';

import {FormsModule, ReactiveFormsModule} from '@angular/forms'
import {MatInputModule} from '@angular/material/input';
import {MatTableModule} from '@angular/material/table';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'

import { MatSliderModule } from '@angular/material/slider';
import { MatButtonModule, MatIconModule } from '@angular/material';
import { WorldcatListComponent } from './worldcat-list/worldcat-list.component';
import { WorldcatResultsComponent } from './worldcat-results/worldcat-results.component';

@NgModule({
  declarations: [
    AppComponent,
    DialogOverviewExampleDialogComponent,
    WorldcatListComponent,
    WorldcatResultsComponent
  ],
  entryComponents: [AppComponent, DialogOverviewExampleDialogComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatButtonModule,
    MatIconModule
  ],
  bootstrap: [AppComponent],
  providers: [BackendApiService]
})
export class AppModule { }
